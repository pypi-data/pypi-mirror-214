# coding:utf-8
import sys

if sys.platform == "win32":
    from .win32_utils import WindowsMoveResize as MoveResize
else:
    raise SystemExit('Not win11 platform')


def startSystemMove(window, globalPos):
    """ resize window

    Parameters
    ----------
    window: QWidget
        window

    globalPos: QPoint
        the global point of mouse release event
    """
    MoveResize.startSystemMove(window, globalPos)


def starSystemResize(window, globalPos, edges):
    """ resize window

    Parameters
    ----------
    window: QWidget
        window

    globalPos: QPoint
        the global point of mouse release event

    edges: `Qt.Edges`
        window edges
    """
    MoveResize.starSystemResize(window, globalPos, edges)
