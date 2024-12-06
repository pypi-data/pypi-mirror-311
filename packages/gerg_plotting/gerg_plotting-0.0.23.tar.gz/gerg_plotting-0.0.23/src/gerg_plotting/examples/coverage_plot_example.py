from gerg_plotting.plotting_classes.CoveragePlot import CoveragePlot
from gerg_plotting.tools import custom_legend_handles

import matplotlib.pyplot as plt


def coverage_plot_example():
    cmap = plt.get_cmap('tab20')
    # domains = create_combinations_with_underscore(['Basin', 'Regional', 'Local'])
    # domains.extend(['All'])
    # print(domains)
    domains = ['Regional_Local', 'All', 'Local', 'Basin_Regional', 'Basin_Local', 'Basin', 'Regional']
    colors_light = [cmap(15),cmap(5),cmap(3),cmap(1),'yellow','pink','gold']
    colors_dark = [cmap(14),cmap(4),cmap(2),cmap(0),'yellow','pink','gold']

    colors = colors_light
    domain_colors = {key:value for key,value in zip(domains,colors)}
    # Define the x and y labels
    x_labels = ['Seconds','Minutes','Hours','Days','Weeks','Months','Years','Decades']
    y_labels = ['Surface','10-100\nMeters','100-500\nMeters','Below 500\nMeters','Benthic']
    # Init the coverage plotter
    plotter = CoveragePlot(figsize=(12,6),x_labels=x_labels,y_labels=y_labels,
                           grid_color='k',grid_linestyle='--',grid_linewidth=1,
                           arrow_facecolor='coverage_facecolor',arrow_linewidth=1,arrow_width=0.06,arrow_head_width=0.12,
                           coverage_fontsize=10.5,coverage_linewidth=1.25,coverage_alpha=1,coverage_min_rectangle_height=0.25)
    # All Depths
    plotter.add_coverage(x_range=['Hours','Decades'],y_range=['Surface','Benthic'],label='Agency',label_position=(4,3.3),fc=domain_colors['All'])
    plotter.add_coverage(x_range=['Seconds','Decades'],y_range=['Surface','Benthic'],label='Academic',label_position=(3.5,2),fc=domain_colors['All'])
    plotter.add_coverage(x_range=['Days','Months'],y_range=['Surface','Benthic'],label='Consultants',label_position=(4.5,1.7),fc=domain_colors['Regional_Local'])
    plotter.add_coverage(x_range=['Days','Years'],y_range=['Surface','Benthic'],label='Regulatory',label_position=(4.5,2.3),fc=domain_colors['Regional_Local'])
    plotter.add_coverage(x_range=['Days','Decades'],y_range=['Surface','Benthic'],label='Oil and Gas',label_position=(4.5,3),fc=domain_colors['All'])
    plotter.add_coverage(x_range=['Months','Years'],y_range=['Surface','Benthic'],label='Fisheries',label_position=(6,2.75),fc=domain_colors['Regional_Local'])
    plotter.add_coverage(x_range='Decades',y_range=['Surface','Benthic'],label='Climate\nScience',label_position=(7.5,1.7),fc=domain_colors['Basin_Regional'])
    plotter.add_coverage(x_range=['Hours','Weeks'],y_range=['Surface','Benthic'],label='Disaster',label_position=(4,2.75),fc=domain_colors['All'])
    # Surface
    plotter.add_coverage(x_range=['Hours','Days'],y_range=[-0.5,-0.5],label='Search and Rescue',fc=domain_colors['Local'])
    plotter.add_coverage(x_range=['Days','Decades'],y_range=[0.25,0.25],label='Wind and Algal Blooms',fc=domain_colors['Local'])
    plotter.add_coverage(x_range=['Weeks','Months'],y_range=[-0.5,-0.5],label='Shipping',label_position=(4.6,-0.375),fc=domain_colors['Basin'])
    plotter.add_coverage(x_range=['Days','Years'],y_range=[-0.15,-0.15],label='Recreational',label_position=(4.5,-0.025),fc=domain_colors['Basin'])
    # 10-100m
    plotter.add_coverage(x_range=['Months','Years'],y_range=['Surface','100-500 Meters'],label='CCUS',label_position=(6,0.775),fc=domain_colors['Local'])
    plotter.add_coverage(x_range=['Hours','Weeks'],y_range=[0.65,0.65],label='Hurricane Forcasting',fc=domain_colors['All'])
    plotter.add_coverage(x_range=['Days','Years'],y_range=[1,1],label='Hypoxia',fc=domain_colors['Regional_Local'])
    plotter.plot()

    handles = custom_legend_handles(domain_colors.keys(),domain_colors.values())
    plotter.fig.legend(handles=handles,bbox_to_anchor=(0.25, 0.39),framealpha=1,title='Domains')

    plotter.fig.tight_layout()

    plotter.fig.savefig('example_plots/coverage_plot_example.png',dpi=600)


if __name__ == "__main__":
    coverage_plot_example()
