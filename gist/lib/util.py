import sublime
import os
import json
import webbrowser

def get_gists_cache(settings):
    cache_dir = os.path.join(settings["workspace"], ".cache", "gists.json")
    if not os.path.isfile(cache_dir): return
    return json.loads(open(cache_dir).read())

def add_gists_to_cache(gists):
    """Add gist the caches"""
    
    settings = get_settings()
    outputdir = os.path.join(settings["workspace"], ".cache")
    cachedir = os.path.join(outputdir, "gists.json")

    if not os.path.exists(outputdir):
        os.makedirs(outputdir)
        
    with open(outputdir + "/gists.json", "w") as fp:
        fp.write(json.dumps(gists, indent=4))

def get_settings():
    """ Load settings from sublime-settings"""
    
    settings = {}
    s = sublime.load_settings("HaoGist.sublime-settings")
    settings["token"] = s.get("token")
    settings["debug_mode"] = s.get("debug_mode", False)
    settings["auto_update_on_save"] = s.get("auto_update_on_save", True)
    settings["default_chrome_path"] = s.get("default_chrome_path", "")
    settings["delay_seconds_for_hiding_panel"] = s.get("delay_seconds_for_hiding_panel", 1)
    settings["http_proxies"] = s.get("http_proxies", {})

    # If user didn't set the workspace
    workspace = s.get("workspace")
    if not workspace: 
        workspace = os.path.join(sublime.packages_path(), "User", "HaoGist")
    settings["workspace"] = workspace

    return settings

def open_with_browser(show_url, use_default_chrome=True):
    """ Utility for open file in browser

    Arguments:

    * use_default_browser -- optional; if true, use chrome configed in settings to open it
    """

    settings = get_settings()
    browser_path = settings["default_chrome_path"]
    if not use_default_chrome or not os.path.exists(browser_path):
        webbrowser.open_new_tab(show_url)
    else:
        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(browser_path))
        webbrowser.get('chrome').open_new_tab(show_url)

def close_view_by_filename(file_name):
    view = get_view_by_file_name(file_name)
    if view:
        sublime.active_window().focus_view(view)
        sublime.active_window().run_command("close")

def get_view_by_name(view_name):
    """Get view by view name

    Arguments:

    * view_name -- name of view in sublime

    Returns:

    * view -- sublime open tab
    """
    view = None
    for v in sublime.active_window().views():
        if not v.name(): continue
        if v.name() == view_name:
            view = v

    return view

def get_view_by_file_name(file_name):
    """
    Get the view in the active window by the view_name

    Arguments:

    * view_id: view name

    Returns:

    * return: view
    """

    view = None
    for v in sublime.active_window().views():
        if not v.file_name(): continue
        if file_name in v.file_name():
            view = v

    return view

def get_view_by_id(view_id):
    """
    Get the view in the active window by the view_id

    * view_id: id of view
    * return: view
    """

    view = None
    for v in sublime.active_window().views():
        if not v.id(): continue
        if v.id() == view_id:
            view = v

    return view
