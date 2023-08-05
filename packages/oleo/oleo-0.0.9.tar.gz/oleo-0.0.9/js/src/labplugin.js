import {HelloModel, HelloView, NetlistGraphModel, NetlistGraphView, version} from './index';
import {IJupyterWidgetRegistry} from '@jupyter-widgets/base';

export const oleoPlugin = {
  id: 'oleo:plugin',
  requires: [IJupyterWidgetRegistry],
  activate: function(app, widgets) {
      widgets.registerWidget({
          name: 'oleo',
          version: version,
          exports: { 
            HelloModel,
            HelloView,
            NetlistGraphModel,
            NetlistGraphView 
          }
      });
  },
  autoStart: true
};

export default oleoPlugin;
