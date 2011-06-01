/**
 * editor_plugin_src.js
 *
 * Copyright 2009, Moxiecode Systems AB
 * Released under LGPL License.
 *
 * License: http://tinymce.moxiecode.com/license
 * Contributing: http://tinymce.moxiecode.com/contributing
 */

(function() {
	tinymce.create('tinymce.plugins.BBCodePlugin', {
		init : function(ed, url) {
			var t = this, dialect = ed.getParam('bbcode_dialect', 'punbb').toLowerCase();

			ed.onBeforeSetContent.add(function(ed, o) {
				o.content = t['_' + dialect + '_bbcode2html'](o.content);
			});

			ed.onPostProcess.add(function(ed, o) {
				if (o.set)
					o.content = t['_' + dialect + '_bbcode2html'](o.content);

				if (o.get)
					o.content = t['_' + dialect + '_html2bbcode'](o.content);
			});
		},

		getInfo : function() {
			return {
				longname : 'BBCode Plugin',
				author : 'Moxiecode Systems AB',
				authorurl : 'http://tinymce.moxiecode.com',
				infourl : 'http://wiki.moxiecode.com/index.php/TinyMCE:Plugins/bbcode',
				version : tinymce.majorVersion + "." + tinymce.minorVersion
			};
		},

		// Private methods

		// HTML -> BBCode in PunBB dialect
		_punbb_html2bbcode : function(s) {
			s = tinymce.trim(s);

			function rep(re, str) {
				s = s.replace(re, str);
			};

			// example: <strong> to [b]
			rep(/<pre.*?class=\"brush:(.*?);.*?\">/gi,"[code class=$1]");
			rep(/<\/pre>/gi,"[/code]");
			
			rep(/<a.*?href=\"(.*?)\".*?>(.*?)<\/a>/gi,"[url=$1]$2[/url]");			
			rep(/<font.*?color=\"(.*?)\".*?class=\"quoteStyle\".*?>(.*?)<\/font>/gi,"[quote][color=$1]$2[/color][/quote]");
			rep(/<font.*?class=\"quoteStyle\".*?color=\"(.*?)\".*?>(.*?)<\/font>/gi,"[quote][color=$1]$2[/color][/quote]");
			rep(/<span style=\"color: ?(.*?);\">(.*?)<\/span>/gi,"[color=$1]$2[/color]");
			rep(/<font.*?color=\"(.*?)\".*?>(.*?)<\/font>/gi,"[color=$1]$2[/color]");
			rep(/<span style=\"font-size:(.*?);\">(.*?)<\/span>/gi,"[size=$1]$2[/size]");
			rep(/<font>(.*?)<\/font>/gi,"$1");
			rep(/<img.*?src=\"(.*?)\".*?\/>/gi,"[img]$1[/img]");			
			rep(/<span class=\"quoteStyle\">(.*?)<\/span>/gi,"[quote]$1[/quote]");			
			rep(/<strong class=\"quoteStyle\">(.*?)<\/strong>/gi,"[quote][b]$1[/b][/quote]");			
			rep(/<em class=\"quoteStyle\">(.*?)<\/em>/gi,"[quote][i]$1[/i][/quote]");
			rep(/<u class=\"quoteStyle\">(.*?)<\/u>/gi,"[quote][u]$1[/u][/quote]");
			rep(/<\/(strong|b)>/gi,"[/b]");
			rep(/<(strong|b)>/gi,"[b]");
			rep(/<\/(em|i)>/gi,"[/i]");
			rep(/<(em|i)>/gi,"[i]");
			rep(/<\/u>/gi,"[/u]");
			rep(/<span style=\"text-decoration: ?underline;\">(.*?)<\/span>/gi,"[u]$1[/u]");
			rep(/<u>/gi,"[u]");
			rep(/<blockquote[^>]*>/gi,"[quote]");
			rep(/<\/blockquote>/gi,"[/quote]");
			rep(/<h([3-6])[^>]*>/gi,"[h$1]");
			rep(/<\/h([3-6])>/gi,"[/h$1]");
			
			rep(/<br \/>\n/gi,"\n");
			rep(/<br\/>\n/gi,"\n");
			rep(/<br>\n/gi,"\n");

			rep(/\n<br \/>/gi,"\n");
			rep(/\n<br\/>/gi,"\n");
			rep(/\n<br>/gi,"\n");
			
			rep(/<br \/>/gi,"\n");
			rep(/<br\/>/gi,"\n");
			rep(/<br>/gi,"\n");
			rep(/<p.*?>/gi,"");
			rep(/<\/p>/gi,"\n");
			rep(/&nbsp;|\u00a0/gi," ");
			rep(/&quot;/gi,"\"");
			
			
			//rep(/<em class=\"codeStyle\">(.*?)<\/em>/gi,"[code][i]$1[/i][/code]");
			//rep(/<strong class=\"codeStyle\">(.*?)<\/strong>/gi,"[code][b]$1[/b][/code]");
			//rep(/<span class=\"codeStyle\">(.*?)<\/span>/gi,"[code]$1[/code]");
			//rep(/<font.*?class=\"codeStyle\".*?color=\"(.*?)\".*?>(.*?)<\/font>/gi,"[code][color=$1]$2[/color][/code]");
			//rep(/<font.*?color=\"(.*?)\".*?class=\"codeStyle\".*?>(.*?)<\/font>/gi,"[code][color=$1]$2[/color][/code]");
			//rep(/<u class=\"codeStyle\">(.*?)<\/u>/gi,"[code][u]$1[/u][/code]");
			// rep(/&lt;/gi,"<");
			// rep(/&gt;/gi,">");
			// rep(/&amp;/gi,"&");

			return s; 
		},

		// BBCode -> HTML from PunBB dialect
		_punbb_bbcode2html : function(s) {
			s = tinymce.trim(s);

			function rep(re, str) {
				s = s.replace(re, str);
			};

			// example: [b] to <strong>
			rep(/\[\/(.*)\]\n/gi,"[\/$1]");
			rep(/\[b\]/gi,"<strong>");
			rep(/\[\/b\]/gi,"</strong>");
			rep(/\[i\]/gi,"<em>");
			rep(/\[\/i\]/gi,"</em>");
			rep(/\[u\]/gi,"<u>");
			rep(/\[\/u\]/gi,"</u>");
			rep(/\[url=(.*?)\](.*?)\[\/url\]/gi,"<a href=\"$1\">$2</a>");
			rep(/\[url\](.*?)\[\/url\]/gi,"<a href=\"$1\">$1</a>");
			rep(/\[img.*?\](.*?)\[\/img\]/gi,"<img src=\"$1\" />");
			rep(/\[color=(.*?)\](.*?)\[\/color\]/gi,"<font color=\"$1\">$2</font>");
			rep(/\[quote.*?\](.*?)\[\/quote\]/gi,"<span class=\"quoteStyle\">$1</span>&nbsp;");
			rep(/\[h3\](.*?)\[\/h3\]/gi,"<h3>$1</h3>");
			rep(/\[h4\](.*?)\[\/h4\]/gi,"<h4>$1</h4>");
			rep(/\[h5\](.*?)\[\/h5\]/gi,"<h5>$1</h5>");
			rep(/\[h6\](.*?)\[\/h6\]/gi,"<h6>$1</h6>");
			rep(/\[code.*?class=(.*?)\]/gi,"<pre class=\"brush:$1;\">");
			rep(/\[\/code\]/gi,"</pre>");
			
			rep(/\n/gi,"<br />");

			return s; 
		}
	});

	// Register plugin
	tinymce.PluginManager.add('bbcode', tinymce.plugins.BBCodePlugin);
})();