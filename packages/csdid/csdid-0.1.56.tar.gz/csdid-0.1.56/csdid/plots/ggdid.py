from csdid.plots.gplot import gplot, splot

import numpy as np
import pandas as pd
from scipy.stats import norm
from plotnine import ggplot, facet_wrap

def ggdid_attge(did_object, 
                ylim=None, 
                xlab=None, 
                ylab=None, 
                title="Group",
                xgap=1, 
                ncol=1, 
                legend=True, 
                group=None, 
                ref_line=0,
                theming=True, 
                grtitle="Group", 
                **kwargs):
  
  grp = did_object['group']
  t_i = did_object['t']

  G = len(np.unique(grp))
  Y = len(np.unique(t_i))
  g = np.unique(grp)[np.argsort(np.unique(grp))].astype(int)
  y = np.unique(t_i)

  results = pd.DataFrame({'year': np.tile(y, G)})
  results['group'] = np.repeat(g, Y)
  results['grtitle'] = grtitle + ' ' + results['group'].astype(str)
  results['att'] = did_object['att']
  results['att_se'] = did_object['se']
  results['post'] = np.where(results['year'] >= grp, 1, 0)
  results['year'] = results['year']
  results['c'] = did_object['c']

  results = results.query(
    'group in @group'
  )

  if group is None:
    group = g
    if any(group not in g for group in group):
      raise ValueError("Some of the specified groups do not exist in the data. Reporting all available groups.")
      group = g

  mplots = gplot(results, ylim, xlab, ylab, title, xgap, legend, ref_line, theming) + \
              facet_wrap('~ grtitle', ncol=ncol, scales='free')
  return mplots