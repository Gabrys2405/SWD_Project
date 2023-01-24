
from typing import TypeVar, Callable, Tuple, List
import io
from matplotlib import pyplot as plt

_T = TypeVar("_T")


def execute_and_get_buffers(func: Callable[[], _T]) -> Tuple[List[io.BytesIO], _T]:
    """Na pewien czas podmienia funkcję plt.show(), aby wyłapać wykresy i zapisać je do buforów."""

    print("Buffering figures...")
    imgs: List[io.BytesIO] = []

    def custom_show(fig = None):
        if fig == None:
            fig = plt.gcf()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        imgs.append(buf)
        print(len(buf.getvalue()))
    
    old_show = plt.show
    plt.show = custom_show
    ret = func()
    plt.show = old_show

    print(f"Buffered {len(imgs)} figure(s)!")
    return imgs, ret
