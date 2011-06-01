$(function(){
	var config = {
		script_url : '/public/tiny_mce/tiny_mce.js',
		theme : "advanced",
        mode : "none",
        plugins : "preview,bbcode,syntaxhl",
        theme_advanced_buttons1 : "newdocument,|,bold,formatselect,|,undo,redo,|,link,unlink,image,cleanup,code,|,preview,syntaxhl",
        theme_advanced_buttons2 : "",
        theme_advanced_buttons3 : "",
        theme_advanced_toolbar_location : "top",
        theme_advanced_toolbar_align : "center",
        theme_advanced_statusbar_location : "bottom",
        //theme_advanced_styles : "Code=codeStyle;Quote=quoteStyle;Code=class",
        entity_encoding : "raw",
        //extended_valid_elements : "a[href],p,br,img[src],span,em,strong,i,blockquote,h3,h4,h5,h6,pre[class]",
		//valid_elements: 'a,p,br,img,span,em,strong,pre,i,blockquote,h3,h4,h5,h6',
		valid_elements: "strong/b,a[!href|target],p,br,h3,h4,h5,h6,pre[class],img[!src|title|alt|width|height]",
		theme_advanced_blockformats : "p,h3,h4,h5,h6",
        add_unload_trigger : false,
        remove_linebreaks : false,
        inline_styles : false,
		force_br_newlines : true,
		force_p_newlines : false,
        forced_root_block : '',
        content_css : "/public/css/editor.css"

	};
			
	$('textarea.editor').tinymce(config);
	
	function path() {
		var args = arguments, result = [];  
		for(var i = 0; i < args.length; i++) {
			result.push(args[i].replace('@', '/public/syntaxhighlighter/scripts/'));
		}
		return result
	};
	 
	SyntaxHighlighter.autoloader.apply(null, path(
		'bash shell             @shBrushBash.js',
		'cpp c                  @shBrushCpp.js',
		'css                    @shBrushCss.js',
		'diff patch pas         @shBrushDiff.js',
		'js jscript javascript  @shBrushJScript.js',
		'php                    @shBrushPhp.js',
		'perl pl                @shBrushPerl.js',
		'text plain             @shBrushPlain.js',
		'py python              @shBrushPython.js',
		'ruby rails ror rb      @shBrushRuby.js',
		'sql                    @shBrushSql.js'
	));
	
	SyntaxHighlighter.all();
	
	$("a.tab").click( function(){
		var table_href = $(this).attr('href');
		$(".entry_list").css('display', 'none');
		$(table_href).css('display', '');
	});
});