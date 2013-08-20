import ashiba   
from ashiba.plot import plt

from github import daily_commit_timeline, weekly_commit_timeline

def mybutton__click(dom):

    user = dom['usersearch']['value']
    repo = dom['reposearch']['value']

    ts = weekly_commit_timeline(user, repo)
    ts2 = daily_commit_timeline(user, repo)

    ts.plot()
    plt.title("Weekly commits for %s".format('Github') %repo)
    dom['img_plot'].set_image(plt.get_svg(), 'svg')

    ts2.plot()
    plt.title("Daily commits for %s".format('Github') % repo)
    dom['img_plot2'].set_image(plt.get_svg(), 'svg')


    plt.close()
 
    return dom
