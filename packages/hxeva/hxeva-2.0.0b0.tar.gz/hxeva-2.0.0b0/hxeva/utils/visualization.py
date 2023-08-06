# coding: utf-8
"""
Function

----------------------------------
Version    : 0.0.1
Date       : 2023/5/9   14:52
----------------------------------
Author     : April
Contact    : fanglwh@outlook.com
"""

__all__ = ['Precipitation']

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm


class Precipitation(object):
    PRE = dict(r=[255,  167,  61,  92,   0,    3,    249,  232, 159, 80],
               g=[255,  239,  166, 185,  1,    114,  5,    74,  56,  2],
               b=[255,  140,  7,   253,  250,  77,   241,  0,   21,  0],
               hex=["none", "#A7EF8C", "#3DA607", "#5CB9FD", "#0001FA", "#03724D", "#F905F1", "#E84A00",
                  "#9F3815", "#500200"]
               )
    PRE_CMAP = ListedColormap(PRE["hex"])

    @classmethod
    def contourf(cls, data, **kwargs):
        """

        Args:
            data:
            **kwargs:

        Returns:

        """
        dpi = kwargs.pop('dpi', 300)
        figsize = kwargs.pop('figsize', (10, 10))
        save_path = kwargs.pop('save_path', './precipitation.png')
        threshold = kwargs.pop('threshold', [0, 0.1, 2, 4, 6, 8, 10, 20, 25, 50, 999])

        kwargs.update(dict(cmap=cls.PRE_CMAP,
                           norm=BoundaryNorm(threshold, cls.PRE_CMAP.N)))


        fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
        img = ax.contourf(data, levels=threshold, **kwargs)
        plt.colorbar(img)
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()
