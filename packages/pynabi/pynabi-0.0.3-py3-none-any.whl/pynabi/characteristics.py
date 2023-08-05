from ._common import Stampable as _S


def _dm(name: str):
    def method(self: 'Dielectric', value: float):
        assert value > 0, "Dielectric carachteristrucs must be positive"
        self._d[name] = value
    return method


class Dielectric(_S):
    def __init__(self) -> None:
        super().__init__()
        self._d: dict[str, float] = dict()

    def stamp(self, index: int):
        s = index or ''
        return '\n'.join(f"die{k}{s} {v}" for k, v in self._d.items())
    
    EnergyCutoff = _dm("cut")
    Gap = _dm("gap")
    Lambda = _dm("lam")
    ScreeningLength = _dm("lng")
    Constant = _dm("mac")
    MixingFactor = _dm("mix")
    MagnetizationMixingFactor = _dm("mixmag")