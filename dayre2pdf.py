import argparse, sys
import pulldata
import activity
import parse_dayre
from discover import *
import pickle
import cmd


# def get_args():
    # parser = argparse.ArgumentParser(description='Tool for creating a PDF from a user\'s Dayre data.')
    # parser.add_argument('username', help='Username of user')
    # parser.add_argument('-d', '--dump', action='store_true', help='Include to simply dump all user day and image data as HTML')
    
    # return parser.parse_args()

# def main():
    # # parse args, get user name
    # parser = get_args()
    # print('User: %s' % parser.username)
    
    # if parser.dump:
        # show_users_pickle(parser.username)
        # sys.exit(0)
        
    # get_data(parser.username)
    
def get_data(username):
    print('Initiating spider')
    try:
        # create dayre_puller
        ds = dayre_spider(username)
    except UserNotFoundError as e:
        print('Exception occurred: %s' % e.message)
        return
    
    ds.process_profile()
    ds.discover_posts()
    ds.read_post_data()
    ds.download_images()
    
    return ds.get_userdata()
    
def show_users_pickle(username):
    user = load_user_data('%s_data.pickle' % username)
    print(user['name'])
    print(user['activity'])

def save_user_data(data, filename):
    with open(filename, 'w') as f:
        pickle.dump(data, f)
    
def load_user_data(filename):
    data = ''
    if not os.path.exists(filename):
        return None
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    return data
    
def most_recent_day(activity):
    """ Searches an activity for the most recent day. Returns a (yyyy, ddd) tuple """
    max_year = max(activity.years.keys())
    max_day = max(activity.years[max_year].days.keys())
    
    return (max_year, max_day)
    
def search_for_new_comments(activity):
    """ Searches all stored data links for new comments 
          adds any new comments to activity """
    # TODO
    return
    
def get_new_comments(activity, year, day):
    """ Searches the selected day for new comments, retrieving any """
    # TODO
    return
    
    
class d2pcli(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.data = ''
        self.username = ''
        
    def check_user(self):
        if self.username == '':
            print('No user set')
            return False
        return True

    def check_data(self):
        if self.data == '':
            print('no data')
            return False
        return True
        
    def do_autoget(self, line):
        """ auto_get -- Finds and pulls all dayre data for currently set username, saving images and dumping a data file """
        if not self.check_user(): return
        get_data(self.username)
        
    def do_set(self, username):
        """ set -- Selects the given user """
        self.username = username
        print('set user to: %s' % self.username)
        
    def do_load(self, line):
        """ load -- Reads the selected user's data file if it exists. Replaces any open user files """
        if not self.check_user(): return
        filename = '%s_data.pickle' % self.username
        if not os.path.exists(filename):
            print('file "%s" not found' % filename)
            return
        self.data = load_user_data(filename)
        print ('load complete')
        
    def do_save(self, line):
        """ Saves the currently loaded user's data to file. """
        if not self.check_user(): return
        filename = '%s_data.pickle' % self.username
        save_user_data(user, filename)
        print ('save complete')
        
    def do_summary(self, line):
        """ Prints a summary of user """
        if not self.check_user(): return
        if self.data == '':
            print('no data')
            return
        d = self.data
        return 'Name: %s\nURL: %s\nBio: %s\n%s ' % (d['name'], d['url'], d['bio'], d['activity'])
        
    def do_lastday(self, line):
        """ Prints the most recent day in stored data """
        if not self.check_user(): return
        if not self.check_data(): return
        print(most_recent_day(self.data['activity']))
        
    def do_tex(self, line):
        """ Exports the selected data to a tex file """
        print('Coming soon..!')
        
    def do_EOF(self, line):  # C-d exits
        print('exiting..')
        return True
    

if __name__ == "__main__":
    # main()
    d2pcli().cmdloop()