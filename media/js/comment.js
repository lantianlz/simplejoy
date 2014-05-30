/**
 * @attention 评论模块的js封装
 * @author lizheng
 * @date 2011-11-28
 */

function get_comment(outerobj_type, outerobj_id, comment_show_type, page, can_create_comment_permission)
{
	/**
     *@attention:get comment
     */
	//定义全局变量供callback函数调用
	g_outerobj_type = outerobj_type;
	g_outerobj_id = outerobj_id;
	g_page = page || '1';
	
	
	var par_ele = jQ('#' + g_outerobj_type + '_' + g_outerobj_id);
	var comment_frame = par_ele.find('#comment_frame_id');
	if(comment_frame.length > 0)
	{
		comment_frame.remove();
		if(!page)
		{
			return;
		}
	}
	par_ele.append(jQ('<div id="comment_frame_id"><img class="none" style="margin:0 auto;" src="' + media + '/img/loading.gif" alt="......" id="more_feed_img_id"></div>'));
	par_ele.find('#more_feed_img_id').show();
	var postData = {'outerobj_type':outerobj_type, 'outerobj_id':outerobj_id, 'comment_show_type':comment_show_type};
	if(page != undefined && page != '')
	{
		postData.page = page;
	}
	if(can_create_comment_permission != undefined && can_create_comment_permission != '')
	{
		postData.can_create_comment_permission = can_create_comment_permission;
	}
	var url = '/comment/get_outerobj_comment';
	ajaxSend(url, postData, get_comment_callback, '', 'html');
}



function get_comment_callback(data)
{
	/**
	 * @attention:获取评论回调函数
	 */
	
	var par_ele = jQ('#' + g_outerobj_type + '_' + g_outerobj_id);
	
	if((g_page + '') != '1')
	{
		//设置窗口位置信息
		var pos = par_ele.find('#comment_frame_id').offset();
		jQ(window).scrollTop(pos.top - 30);
	}
	
	par_ele.find('#comment_frame_id').remove();
	par_ele.append(jQ(data));
	comment_register_shortcut();
}


function create_comment(outerobj_type, outerobj_id, comment_show_type, ajax_obj_id)
{
	/**
     *@attention:create comment
     */
	g_comment_show_type = comment_show_type;
	var content = jQ('#comment_content_id_' + outerobj_id).val();
	var postData = {'outerobj_type':outerobj_type, 'outerobj_id':outerobj_id, 'content':content, 
					'comment_show_type':comment_show_type, 'email':jQ('#email').val(), 'nick':jQ('#nick').val(),
					'user_href':jQ('#user_href').val()
				   };
	var url = '/comment/add';
	g_ajax_processing_obj_id = ajax_obj_id || 'create_comment_id';
	
	ajaxSend(url, postData, create_comment_callback, '', 'html');
}



function create_comment_callback(data)
{
	if(data.indexOf('flag') != -1)
	{
		eval('data=' + data);
		if(data['flag'] != 0)
		{
			alert(data['result']);
			return;
		}
	}
	if(data.indexOf('$') != 0)
	{
		jQ('#comment_content_id_' + g_outerobj_id).val('');
		var par_ele = jQ('#' + g_outerobj_type + '_' + g_outerobj_id + '>#comment_frame_id');
		var obj = jQ(data);
		par_ele.find('#division_id').after(obj);
		obj.hide().fadeIn();
		
		//跳转位置
		if(g_comment_show_type == '0' || g_comment_show_type == '2')
		{
			var pos = par_ele.find('dl:eq(0)').offset();
			jQ(window).scrollTop(pos.top - 30);
		}
	}
	else
	{
		alert(data.slice(1));
	}
}


function remove_comment(id)
{
	/**
     *@attention:remove comment
     */
	if(!confirm('确定删除吗？'))
	{
		return;
	}
	var postData = {'id':id};
	var url = '/comment/remove';
	ajaxSend(url, postData, remove_comment_callback);
}


function remove_comment_callback(data)
{
	if(data['flag'] == '0')
	{
		var id = data['result'];
		jQ('#comment_' + id).fadeOut();
	}
	else
	{
		alert(data['result']);
	}
}


function click_reply(nick)
{
	jQ('#comment_content_id_' + g_outerobj_id).focus().val('回复@' +　nick + ': ');
}



function comment_register_shortcut()
{
	/**
	 * @attention:注册快捷键
	 */
	register_shortcut(jQ('#comment_frame_id textarea'), jQ('#create_comment_id'));
}

