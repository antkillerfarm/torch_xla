import torch
import torch_xla.core.xla_model as xm
from torch_xla import runtime as xr
from typing import Any
import warnings


class autocast(torch.amp.autocast_mode.autocast):
  r"""
  `torch.autocast` for XLA backend devices. See :class:`torch.autocast`.
  ``torch_xla.amp.autocast(device, **kwargs)`` is equivalent to
<<<<<<< HEAD
  ``torch.autocast("xla", **kwargs)`` for XLA:GPU and XLA:TPU for dtype torch.bfloat16,
  ``torch.autocast("cuda", **kwargs)`` for XLA:GPU and other dtypes.
=======
  ``torch.autocast("xla", **kwargs)`` for XLA:TPU and XLA:GPU backends.
>>>>>>> 01834d7d6 (Enable autocast for XLA:GPU)
  """

  def __init__(self,
               device,
               enabled: bool = True,
               dtype: torch.dtype = None,
               cache_enabled: bool = True):
    assert 'xla' in device.__str__(
    ), "torch_xla.autocast is available for XLA:TPU, XLA:GPU"
    xla_device = xm.xla_device_hw(device)
    if xla_device in ['TPU', 'GPU']:
      if dtype is None:
        dtype = torch.bfloat16
      if dtype != torch.bfloat16:
        error_message = "In torch_xla autocast, but the target dtype is not supported. Disabling autocast.\n"
        error_message += (
            "torch_xla Autocast only supports dtype of torch.bfloat16 currently."
        )
        warnings.warn(error_message)
        enabled = False
      self._dtype = dtype
      super().__init__(
          "xla",
          enabled=enabled,
          dtype=self._dtype,
          cache_enabled=cache_enabled)
    else:
      print(
          'Warning: AMP only supported for XLA:TPU and XLA:GPU. Ignoring autocast.'
      )

  def __enter__(self):
    # This ensures that xla autocast is enabled even for XLA:GPU, which calls
    # `torch.amp.autocast_mode.autocast` with `cuda` backend.
    if self._xla_device == 'GPU':
      self.prev = torch.is_autocast_xla_enabled()  # type: ignore[attr-defined]
      self.prev_dtype = torch.get_autocast_xla_dtype(
      )  # type: ignore[attr-defined]
      torch.set_autocast_xla_enabled(self._enabled)
      torch.set_autocast_xla_dtype(self._dtype)
    return super().__enter__()

  def __exit__(self, exc_type: Any, exc_val: Any,
               exc_tb: Any):  # type: ignore[override]
    if self._xla_device == 'GPU':
      torch.set_autocast_xla_enabled(self.prev)
      torch.set_autocast_xla_dtype(self.prev_dtype)
    return super().__exit__(exc_type, exc_val, exc_tb)

  def __call__(self, func):
    return super().__call__(func)
