__author__ = "Damon May"

from typing import List
from matplotlib.figure import Figure
from jamstats.data.game_data import DerbyGame
import logging
from jamstats.plots.jamplots import (
        plot_game_summary_table,
        plot_game_teams_summary_table,
        plot_cumulative_score_by_jam,
        plot_jam_lead_and_scores_period1,    
        plot_jam_lead_and_scores_period2,
        plot_jammers_by_team,
        plot_lead_summary,
        histogram_jam_duration,
        plot_team_penalty_counts,
        plot_roster_with_jammerpivot,
)
from jamstats.plots.skaterplots import (
    plot_jammer_stats_team1,
    plot_jammer_stats_team2,
    plot_skater_stats_team1,
    plot_skater_stats_team2,
)
from jamstats.plots.plot_util import prepare_to_plot, DEFAULT_THEME
from jamstats.util.resources import (
    get_jamstats_logo_image,
    get_jamstats_version
)
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import pyplot as plt
from PIL import Image
import io


logger = logging.Logger(__name__)

def save_game_plots_to_pdf(derby_game: DerbyGame,
                           out_filepath: str,
                           anonymize_names: bool = False,
                           theme: str = DEFAULT_THEME) -> None:
    """Read in a jams .tsv file, make all the plots, write to a .pdf

    Args:
        in_filepath (str): jams .tsv filepath
        out_filepath (str): output .pdf filepath
        anonymize_names (bool): anonymize skater names
    """
    prepare_to_plot(theme=theme)
    figures = make_all_plots(derby_game, anonymize_names=anonymize_names)
    pdfout = PdfPages(out_filepath)
    logging.debug(f"Saving {len(figures)} figures to {out_filepath}")
    for figure in figures:
        pdfout.savefig(figure)
    pdfout.close()
    logging.debug(f"Wrote {out_filepath}")


def make_all_plots(derby_game: DerbyGame,
                   plot_skaterplots: bool = True,
                   anonymize_names: bool = False) -> List[Figure]:
    """Build all plots, suitable for exporting to a .pdf.

    Plot the simplest summary plots first, then the skater plots, then the advanced plots.

    Args:
        derby_game (DerbyGame): a derby game
        plot_skaterplots (bool): Plot the plots with individually identifying skater info?
    Returns:
        List[Figure]: figures
    """
    figures = []

    # plot basic plots
    basic_plots = [
        plot_game_summary_table,
        plot_game_teams_summary_table,
        plot_cumulative_score_by_jam,
        plot_team_penalty_counts
    ]

    for plot_func in basic_plots:
        try:
            logger.info(f"Plotting {plot_func.__name__}")
            f = plot_func(derby_game)
            figures.append(f)
        except Exception as e:
            logger.warn(f"Failed to make jam plot {plot_func.__name__}: {e}")

    # plot skater plots
    if plot_skaterplots:
        for plot_func in [plot_jammer_stats_team1, plot_jammer_stats_team2,
                          plot_skater_stats_team1, plot_skater_stats_team2]:
            try:
                logger.info(f"Plotting {plot_func.__name__}")
                f = plot_func(derby_game, anonymize_names=anonymize_names)
                figures.append(f)
            except Exception as e:
                logger.warn(f"Failed to make skater plot {plot_func.__name__}: {e}")

    # plot advanced plots
    advanced_plots = []
    advanced_plots.append(plot_jam_lead_and_scores_period1)
    if max(derby_game.pdf_jams_data.PeriodNumber) >= 2:
        advanced_plots.append(plot_jam_lead_and_scores_period2)
    advanced_plots.extend([
        plot_jammers_by_team,
        plot_lead_summary,
        histogram_jam_duration,
        plot_roster_with_jammerpivot,
        ])

    for plot_func in advanced_plots:
        try:
            logger.info(f"Plotting {plot_func.__name__}")
            f = plot_func(derby_game)
            figures.append(f)
        except Exception as e:
            logger.warn(f"Failed to make jam plot {plot_func.__name__}: {e}")
    
    # add jamstats version annotation
    for f in figures:
        f.axes[0].annotate(text=f"jamstats version {get_jamstats_version()}",
                           xy=[5, 5], xytext=[5, 5], textcoords="figure pixels", size="x-small")

    # add logo to table plots.
    im_bytes = get_jamstats_logo_image()
    #im = plt.imread(im_bytes)
    im = Image.open(io.BytesIO(im_bytes))
    for f in figures[:2]:
        newax = f.add_axes([0.425,0.9,0.15,0.15], anchor='SE', zorder=1)
        newax.axis('off')
        newax.imshow(im)
    return figures