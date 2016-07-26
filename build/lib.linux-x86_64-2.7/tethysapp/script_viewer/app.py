from tethys_sdk.base import TethysAppBase, url_map_maker


class ScriptViewer(TethysAppBase):
    """
    Tethys app class for R Script Viewer.
    """

    name = 'Script Viewer'
    index = 'script_viewer:home'
    icon = 'script_viewer/images/script.png'
    package = 'script_viewer'
    root_url = 'script-viewer'
    color = '#3498db'
    description = 'Place a brief description of your app here.'
    enable_feedback = False
    feedback_emails = []

        
    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)
        url_maps = (UrlMap(name='home',
                           url='script-viewer',
                           controller='script_viewer.controllers.home'),
                    UrlMap(name='chart_data',
                           url='chart_data/{src}/{res_id}',
                           controller='script_viewer.controllers.chart_data'),
                     UrlMap(name='save_file',
                           url='save_file/{src}/{res_id}/{file_name}/{save_type}',
                           controller='script_viewer.controllers.save_file'),
                    UrlMap(name='delete_file',
                           url='delete_file/{src}/{res_id}/{file_name}',
                           controller='script_viewer.controllers.delete_file'),

        )
        return url_maps


