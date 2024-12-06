/**
 * date: 2023-06-03
 * author: Peter
 * from: layuimini
 */
layui.define(["jquery", "layer", "util", "element", "laytpl",], function (exports) {
    let $ = layui.$;
    let layer = layui.layer;
    let laytpl = layui.laytpl;
    let element = layui.element;
    let escape = layui.util.escape;

    let miniTab = {
        /**
         * 初始化tab
         * @param options
         */
        render: function (options) {
            options.filter = options.filter || null;
            options.multiModule = options.multiModule || false;
            options.urlHashLocation = options.urlHashLocation || false;
            options.maxTabNum = options.maxTabNum || 20;
            options.menuList = options.menuList || [];
            options.homeInfo = options.homeInfo || {};
            options.listenSwitchCallback = options.listenSwitchCallback || function () {
            };
            miniTab.listen(options);
            miniTab.listenRoll();
            miniTab.listenSwitch(options);
            miniTab.listenHash(options);
        },

        /**
         * 新建tab窗口
         * @param options.tabId
         * @param options.href
         * @param options.title
         * @param options.isIframe
         * @param options.maxTabNum
         */
        create: function (options) {
            options.tabId = options.tabId || null;
            options.href = options.href || null;
            options.title = options.title || null;
            options.isIframe = options.isIframe || false;
            options.maxTabNum = options.maxTabNum || 20;
            if ($(".layuimini-tab .layui-tab-title li").length >= options.maxTabNum) {
                layer.msg('Tab窗口已达到限定数量，请先关闭部分Tab');
                return false;
            }
            let ele = element;
            if (options.isIframe) ele = parent.layui.element;
            ele.tabAdd('layuiminiTab', {
                title: '<span class="layuimini-tab-active"></span><span>' + options.title + '</span><i class="layui-icon layui-unselect layui-tab-close">ဆ</i>', //用于演示
                content: '<iframe width="100%" height="100%" border="0" frameborder="no" marginwidth="0" marginheight="0"   src="' + options.href + '"></iframe>',
                id: options.tabId
            });
            $('.layuimini-menu-left').attr('layuimini-tab-tag', 'add');
            sessionStorage.setItem('layuiminimenu_' + options.tabId, options.title);
        },


        /**
         * 切换选项卡
         * @param tabId
         */
        change: function (tabId) {
            element.tabChange('layuiminiTab', tabId);
        },

        /**
         * 删除tab窗口
         * @param tabId
         * @param isParent
         */
        delete: function (tabId, isParent) {
            // todo 未知BUG，不知道是不是layui问题，必须先删除元素
            $(".layuimini-tab .layui-tab-title .layui-unselect.layui-tab-bar").remove();

            if (isParent === true) {
                parent.layui.element.tabDelete('layuiminiTab', tabId);
            } else {
                element.tabDelete('layuiminiTab', tabId);
            }
        },

        /**
         * 在iframe层打开新tab方法
         */
        openNewTabByIframe: function (options) {
            options.href = options.href || null;
            options.title = options.title || null;
            let loading = parent.layer.load(0, {shade: false, time: 2 * 1000});
            if (options.href === null || options.href === undefined) options.href = new Date().getTime();
            let checkTab = miniTab.check(options.href, true);
            if (!checkTab) {
                miniTab.create({
                    tabId: options.href,
                    href: options.href,
                    title: options.title,
                    isIframe: true,
                });
            }
            parent.layui.element.tabChange('layuiminiTab', options.href);
            parent.layer.close(loading);
        },

        /**
         * 在iframe层关闭当前tab方法
         */
        deleteCurrentByIframe: function () {
            let ele = $(".layuimini-tab .layui-tab-title li.layui-this", parent.document);
            if (ele.length > 0) {
                let layId = $(ele[0]).attr('lay-id');
                miniTab.delete(layId, true);
            }
        },

        /**
         * 判断tab窗口
         */
        check: function (tabId, isIframe) {
            // 判断选项卡上是否有
            let checkTab = false;
            if (isIframe === undefined || isIframe === false) {
                $(".layui-tab-title li").each(function () {
                    let checkTabId = $(this).attr('lay-id');
                    if (checkTabId != null && checkTabId === tabId) {
                        checkTab = true;
                    }
                });
            } else {
                parent.layui.$(".layui-tab-title li").each(function () {
                    let checkTabId = $(this).attr('lay-id');
                    if (checkTabId != null && checkTabId === tabId) {
                        checkTab = true;
                    }
                });
            }
            return checkTab;
        },

        /**
         * 开启tab右键菜单
         * @param tabId
         * @param left
         */
        openTabRightMenu: function (tabId, left) {
            miniTab.closeTabRightMenu();
            let menuHtml = '<div class="layui-unselect layui-form-select layui-form-selected layuimini-tab-mousedown layui-show" data-tab-id="' + tabId + '" style="left: ' + left + 'px !important">';
            menuHtml += `
                <dl>
                    <dd><a href="javascript:;" layuimini-tab-menu-close="current">关 闭 当 前</a></dd>
                    <dd><a href="javascript:;" layuimini-tab-menu-close="other">关 闭 其 他</a></dd>
                    <dd><a href="javascript:;" layuimini-tab-menu-close="all">关 闭 全 部</a></dd>
                </dl>
                </div>
            `;
            let makeHtml = '<div class="layuimini-tab-make"></div>';
            $('.layuimini-tab .layui-tab-title').after(menuHtml);
            $('.layuimini-tab .layui-tab-content').after(makeHtml);
        },

        /**
         * 关闭tab右键菜单
         */
        closeTabRightMenu: function () {
            $('.layuimini-tab-mousedown').remove();
            $('.layuimini-tab-make').remove();
        },

        /**
         * 查询菜单信息
         * @param href
         * @param menuList
         */
        searchMenu: function (href, menuList) {
            let menu;
            for (let key in menuList) {
                let item = menuList[key];
                if (item.href === href) {
                    menu = item;
                    break;
                }
                if (item.child) {
                    let newMenu = miniTab.searchMenu(href, item.child);
                    if (newMenu) {
                        menu = newMenu;
                        break;
                    }
                }
            }
            return menu;
        },

        /**
         * 监听
         * @param options
         */
        listen: function (options) {
            options = options || {};
            options.maxTabNum = options.maxTabNum || 20;

            /**
             * 打开新窗口
             */
            $('body').on('click', '[layuimini-href]', function () {
                let loading = layer.load(0, {shade: false, time: 2 * 1000});
                let tabId = $(this).attr('layuimini-href'),
                    href = $(this).attr('layuimini-href'),
                    title = $(this).text(),
                    target = $(this).attr('target');

                let el = $("[layuimini-href='" + href + "']", ".layuimini-menu-left");
                layer.close(window.openTips);
                if (el.length) {
                    $(el).closest(".layui-nav-tree").find(".layui-this").removeClass("layui-this");
                    $(el).parent().addClass("layui-this");
                }

                if (target === '_blank') {
                    layer.close(loading);
                    window.open(href, "_blank");
                    return false;
                }

                if (tabId === null || tabId === undefined) tabId = new Date().getTime();
                let checkTab = miniTab.check(tabId);
                if (!checkTab) {
                    miniTab.create({
                        tabId: tabId,
                        href: href,
                        title: title,
                        isIframe: false,
                        maxTabNum: options.maxTabNum,
                    });
                }
                element.tabChange('layuiminiTab', tabId);
                layer.close(loading);
            });

            /**
             * 在iframe子菜单上打开新窗口
             */
            $('body').on('click', '[layuimini-content-href]', function () {
                let loading = parent.layer.load(0, {shade: false, time: 2 * 1000});
                let tabId = $(this).attr('layuimini-content-href'),
                    href = $(this).attr('layuimini-content-href'),
                    title = $(this).attr('data-title'),
                    target = $(this).attr('target');
                if (target === '_blank') {
                    parent.layer.close(loading);
                    window.open(href, "_blank");
                    return false;
                }
                if (tabId === null || tabId === undefined) tabId = new Date().getTime();
                let checkTab = miniTab.check(tabId, true);
                if (!checkTab) {
                    miniTab.create({
                        tabId: tabId,
                        href: href,
                        title: title,
                        isIframe: true,
                        maxTabNum: options.maxTabNum,
                    });
                }
                parent.layui.element.tabChange('layuiminiTab', tabId);
                parent.layer.close(loading);
            });

            /**
             * 关闭选项卡
             **/
            $('body').on('click', '.layuimini-tab .layui-tab-title .layui-tab-close', function () {
                let loading = layer.load(0, {shade: false, time: 2 * 1000});
                let $parent = $(this).parent();
                let tabId = $parent.attr('lay-id');
                if (tabId !== undefined || tabId !== null) {
                    miniTab.delete(tabId);
                }
                layer.close(loading);
            });

            /**
             * 选项卡操作
             */
            $('body').on('click', '[layuimini-tab-close]', function () {
                let loading = layer.load(0, {shade: false, time: 2 * 1000});
                let closeType = $(this).attr('layuimini-tab-close');
                $(".layuimini-tab .layui-tab-title li").each(function () {
                    let tabId = $(this).attr('lay-id');
                    let id = $(this).attr('id');
                    let isCurrent = $(this).hasClass('layui-this');
                    if (id !== 'layuiminiHomeTabId') {
                        if (closeType === 'all') {
                            miniTab.delete(tabId);
                        } else {
                            if (closeType === 'current' && isCurrent) {
                                miniTab.delete(tabId);
                            } else if (closeType === 'other' && !isCurrent) {
                                miniTab.delete(tabId);
                            }
                        }
                    }
                });
                layer.close(loading);
            });

            /**
             * 禁用网页右键
             */
            $(".layuimini-tab .layui-tab-title").unbind("mousedown").bind("contextmenu", function (e) {
                e.preventDefault();
                return false;
            });

            /**
             * 注册鼠标右键
             */
            $('body').on('mousedown', '.layuimini-tab .layui-tab-title li', function (e) {
                let left = $(this).offset().left - $('.layuimini-tab ').offset().left + ($(this).width() / 2),
                    tabId = $(this).attr('lay-id');
                if (e.which === 3) {
                    miniTab.openTabRightMenu(tabId, left);
                }
            });

            /**
             * 关闭tab右键菜单
             */
            $('body').on('click', '.layui-body,.layui-header,.layuimini-menu-left,.layuimini-tab-make', function () {
                miniTab.closeTabRightMenu();
            });

            /**
             * tab右键选项卡操作
             */
            $('body').on('click', '[layuimini-tab-menu-close]', function () {
                let loading = layer.load(0, {shade: false, time: 2 * 1000});
                let closeType = $(this).attr('layuimini-tab-menu-close'),
                    currentTabId = $('.layuimini-tab-mousedown').attr('data-tab-id');
                $(".layuimini-tab .layui-tab-title li").each(function () {
                    let tabId = $(this).attr('lay-id');
                    let id = $(this).attr('id');
                    if (id !== 'layuiminiHomeTabId') {
                        if (closeType === 'all') {
                            miniTab.delete(tabId);
                        } else {
                            if (closeType === 'current' && currentTabId === tabId) {
                                miniTab.delete(tabId);
                            } else if (closeType === 'other' && currentTabId !== tabId) {
                                miniTab.delete(tabId);
                            }
                        }
                    }
                });
                miniTab.closeTabRightMenu();
                layer.close(loading);
            });
        },

        /**
         * 监听tab切换
         * @param options
         */
        listenSwitch: function (options) {
            options.filter = options.filter || null;
            options.multiModule = options.multiModule || false;
            options.urlHashLocation = options.urlHashLocation || false;
            options.listenSwitchCallback = options.listenSwitchCallback || function () {

            };
            element.on('tab(' + options.filter + ')', function (data) {
                let tabId = $(this).attr('lay-id');
                if (options.urlHashLocation) {
                    location.hash = '/' + tabId;
                }
                if (typeof options.listenSwitchCallback === 'function') {
                    options.listenSwitchCallback();
                }
                // 判断是否为新增窗口
                if ($('.layuimini-menu-left').attr('layuimini-tab-tag') === 'add') {
                    $('.layuimini-menu-left').attr('layuimini-tab-tag', 'no')
                } else {
                    $("[layuimini-href]").parent().removeClass('layui-this');
                    if (options.multiModule) {
                        miniTab.listenSwitchMultiModule(tabId);
                    } else {
                        miniTab.listenSwitchSingleModule(tabId);
                    }
                }
                miniTab.rollPosition();
            });
        },

        /**
         * 监听hash变化
         * @param options
         * @returns {boolean}
         */
        listenHash: function (options) {
            options.urlHashLocation = options.urlHashLocation || false;
            options.maxTabNum = options.maxTabNum || 20;
            options.homeInfo = options.homeInfo || {};
            options.menuList = options.menuList || [];
            if (!options.urlHashLocation) return false;
            let tabId = location.hash.replace(/^#\//, '');
            if (tabId === null || tabId === undefined || tabId === '') return false;

            // 判断是否为首页
            if (tabId === options.homeInfo.href) return false;

            // 判断是否为右侧菜单
            let menu = miniTab.searchMenu(tabId, options.menuList);
            if (menu !== undefined) {
                miniTab.create({
                    tabId: tabId,
                    href: tabId,
                    title: menu.title,
                    isIframe: false,
                    maxTabNum: options.maxTabNum,
                });
                $('.layuimini-menu-left').attr('layuimini-tab-tag', 'no');
                element.tabChange('layuiminiTab', tabId);
                return false;
            }

            // 判断是否为快捷菜单
            let isSearchMenu = false;
            $("[layuimini-content-href]").each(function () {
                if ($(this).attr("layuimini-content-href") === tabId) {
                    let title = $(this).attr("data-title");
                    miniTab.create({
                        tabId: tabId,
                        href: tabId,
                        title: title,
                        isIframe: false,
                        maxTabNum: options.maxTabNum,
                    });
                    $('.layuimini-menu-left').attr('layuimini-tab-tag', 'no');
                    element.tabChange('layuiminiTab', tabId);
                    isSearchMenu = true;
                    return false;
                }
            });
            if (isSearchMenu) return false;

            // 既不是右侧菜单、快捷菜单,就直接打开
            let title = sessionStorage.getItem('layuiminimenu_' + tabId) === null ? tabId : sessionStorage.getItem('layuiminimenu_' + tabId);
            miniTab.create({
                tabId: tabId,
                href: tabId,
                title: title,
                isIframe: false,
                maxTabNum: options.maxTabNum,
            });
            element.tabChange('layuiminiTab', tabId);
            return false;
        },

        /**
         * 监听滚动
         */
        listenRoll: function () {
            $(".layuimini-tab-roll-left").click(function () {
                miniTab.rollClick("left");
            });
            $(".layuimini-tab-roll-right").click(function () {
                miniTab.rollClick("right");
            });
        },

        /**
         * 单模块切换
         * @param tabId
         */
        listenSwitchSingleModule: function (tabId) {
            $("[layuimini-href]").each(function () {
                if ($(this).attr("layuimini-href") === tabId) {
                    // 自动展开菜单栏
                    let addMenuClass = function ($element, type) {
                        if (type === 1) {
                            $element.addClass('layui-this');
                            if ($element.hasClass('layui-nav-item') && $element.hasClass('layui-this')) {
                                $(".layuimini-header-menu li").attr('class', 'layui-nav-item');
                            } else {
                                addMenuClass($element.parent().parent(), 2);
                            }
                        } else {
                            $element.addClass('layui-nav-itemed');
                            if ($element.hasClass('layui-nav-item') && $element.hasClass('layui-nav-itemed')) {
                                $(".layuimini-header-menu li").attr('class', 'layui-nav-item');
                            } else {
                                addMenuClass($element.parent().parent(), 2);
                            }
                        }
                    };
                    addMenuClass($(this).parent(), 1);
                    return false;
                }
            });
        },

        /**
         * 多模块切换
         * @param tabId
         */
        listenSwitchMultiModule: function (tabId) {
            $("[layuimini-href]").each(function () {
                if ($(this).attr("layuimini-href") === tabId) {

                    // 自动展开菜单栏
                    let addMenuClass = function ($element, type) {
                        if (type === 1) {
                            $element.addClass('layui-this');
                            if ($element.hasClass('layui-nav-item') && $element.hasClass('layui-this')) {
                                let moduleId = $element.parent().attr('id');
                                $(".layuimini-header-menu li").attr('class', 'layui-nav-item');
                                $("#" + moduleId + "HeaderId").addClass("layui-this");
                                $(".layuimini-menu-left .layui-nav.layui-nav-tree").attr('class', 'layui-nav layui-nav-tree layui-hide');
                                $("#" + moduleId).attr('class', 'layui-nav layui-nav-tree layui-this');
                            } else {
                                addMenuClass($element.parent().parent(), 2);
                            }
                        } else {
                            $element.addClass('layui-nav-itemed');
                            if ($element.hasClass('layui-nav-item') && $element.hasClass('layui-nav-itemed')) {
                                let moduleId = $element.parent().attr('id');
                                $(".layuimini-header-menu li").attr('class', 'layui-nav-item');
                                $("#" + moduleId + "HeaderId").addClass("layui-this");
                                $(".layuimini-menu-left .layui-nav.layui-nav-tree").attr('class', 'layui-nav layui-nav-tree layui-hide');
                                $("#" + moduleId).attr('class', 'layui-nav layui-nav-tree layui-this');
                            } else {
                                addMenuClass($element.parent().parent(), 2);
                            }
                        }
                    };
                    addMenuClass($(this).parent(), 1);
                    return false;
                }
            });
        },

        /**
         * 自动定位
         */
        rollPosition: function () {
            let $tabTitle = $('.layuimini-tab  .layui-tab-title');
            let autoLeft = 0;
            $tabTitle.children("li").each(function () {
                if ($(this).hasClass('layui-this')) {
                    return false;
                } else {
                    autoLeft += $(this).outerWidth();
                }
            });
            $tabTitle.animate({
                scrollLeft: autoLeft - $tabTitle.width() / 3
            }, 200);
        },

        /**
         * 点击滚动
         * @param direction
         */
        rollClick: function (direction) {
            let $tabTitle = $('.layuimini-tab  .layui-tab-title');
            let left = $tabTitle.scrollLeft();
            if ('left' === direction) {
                $tabTitle.animate({
                    scrollLeft: left - 450
                }, 200);
            } else {
                $tabTitle.animate({
                    scrollLeft: left + 450
                }, 200);
            }
        }

    };

    let miniMenu = {
        /**
         * 菜单初始化
         * @param options.menuList   菜单数据信息
         * @param options.multiModule 是否开启多模块
         * @param options.menuChildOpen 是否展开子菜单
         */
        render: function (options) {
            options.menuList = options.menuList || [];
            options.multiModule = options.multiModule || false;
            options.menuChildOpen = options.menuChildOpen || false;
            if (options.multiModule) {
                miniMenu.renderMultiModule(options.menuList, options.menuChildOpen);
            } else {
                miniMenu.renderSingleModule(options.menuList, options.menuChildOpen);
            }
            miniMenu.listen();
        },

        /**
         * 单模块
         * @param menuList 菜单数据
         * @param menuChildOpen 是否默认展开
         */
        renderSingleModule: function (menuList, menuChildOpen) {
            menuList = menuList || [];
            let childOpenClass = '';
            if (menuChildOpen) childOpenClass = ' layui-nav-itemed';
            let leftMenuHtml = this.renderLeftMenu(menuList, {childOpenClass: childOpenClass});
            $('.layui-layout-body').addClass('layuimini-single-module'); //单模块标识
            $('.layuimini-header-menu').remove();
            $('.layuimini-menu-left').html(leftMenuHtml);

            element.init();
        },

        /**
         * 渲染一级菜单
         */
        compileMenu: function (menu, isSub) {
            let menuHtml = '<li {{#if(d.menu){ }} data-menu="{{d.menu}}" {{#}}} class="layui-nav-item menu-li {{d.childOpenClass}} {{d.className}}"  {{#if(d.id){ }}  id="{{d.id}}" {{#}}}> <a {{#if(d.href){ }} layuimini-href="{{d.href}}" {{#}}} {{#if(d.target){ }}  target="{{d.target}}" {{#}}} href="javascript:;">{{#if(d.icon){ }}  <i class="{{d.icon}}"></i> {{#}}} <span class="layui-left-nav">{{d.title}}</span></a>  {{# if(d.children){}} {{- d.children}} {{#}}} </li>';
            if (isSub) {
                menuHtml = '<dd class="menu-dd {{d.childOpenClass}} {{d.className}}"> <a href="javascript:;"  {{#if(d.menu){ }}  data-menu="{{d.menu}}" {{#}}} {{#if(d.id){ }}  id="{{d.id}}" {{#}}} {{#if((!d.child || !d.child.length) && d.href){ }} layuimini-href="{{d.href}}" {{#}}} {{#if(d.target){ }}  target="{{d.target}}" {{#}}}> {{#if(d.icon){ }}  <i class="{{d.icon}}"></i> {{#}}} <span class="layui-left-nav"> {{d.title}}</span></a> {{# if(d.children){}} {{- d.children}} {{#}}}</dd>'
            }
            return laytpl(menuHtml).render(menu);
        },
        compileMenuContainer: function (menu, isSub) {
            let wrapperHtml = '<ul class="layui-nav layui-nav-tree layui-left-nav-tree {{d.className}}" id="{{d.id}}">{{- d.children}}</ul>';
            if (isSub) {
                wrapperHtml = '<dl class="layui-nav-child ">{{- d.children}}</dl>';
            }
            if (!menu.children) {
                return "";
            }
            return laytpl(wrapperHtml).render(menu);
        },
        each: function (list, callback) {
            let array = [];
            for (let i = 0, length = list.length; i < length; i++) {
                array[i] = callback(i, list[i]);
            }
            return array;
        },
        renderChildrenMenu: function (menuList, options) {
            let me = this;
            menuList = menuList || [];
            let html = this.each(menuList, function (idx, menu) {
                if (menu.child && menu.child.length) {
                    menu.children = me.renderChildrenMenu(menu.child, {childOpenClass: options.childOpenClass || ''});
                }
                menu.className = "";
                menu.childOpenClass = options.childOpenClass || ''
                return me.compileMenu(menu, true)
            }).join("");
            return me.compileMenuContainer({children: html}, true)
        },
        renderLeftMenu: function (leftMenus, options) {
            options = options || {};
            let me = this;
            let leftMenusHtml = me.each(leftMenus || [], function (idx, leftMenu) { // 左侧菜单遍历
                let children = me.renderChildrenMenu(leftMenu.child, {childOpenClass: options.childOpenClass});
                return me.compileMenu({
                    href: leftMenu.href,
                    target: leftMenu.target,
                    childOpenClass: options.childOpenClass,
                    icon: leftMenu.icon,
                    title: leftMenu.title,
                    children: children,
                    className: '',
                });
            }).join("");

            return me.compileMenuContainer({
                id: options.parentMenuId,
                className: options.leftMenuCheckDefault,
                children: leftMenusHtml
            });
        },
        /**
         * 多模块
         * @param menuList 菜单数据
         * @param menuChildOpen 是否默认展开
         */
        renderMultiModule: function (menuList, menuChildOpen) {
            menuList = menuList || [];
            let me = this;
            let headerMobileMenuHtml = '',
                leftMenuHtml = '',
                childOpenClass = '',
                leftMenuCheckDefault = 'layui-this',
                headerMenuCheckDefault = 'layui-this';

            if (menuChildOpen) childOpenClass = ' layui-nav-itemed';
            let headerMenuHtml = this.each(menuList, function (index, val) { //顶部菜单渲染
                let menu = 'multi_module_' + index;
                let id = menu + "HeaderId";
                let topMenuItemHtml = me.compileMenu({
                    className: headerMenuCheckDefault,
                    menu: menu,
                    id: id,
                    title: val.title,
                    href: "",
                    target: "",
                    children: ""
                });
                leftMenuHtml += me.renderLeftMenu(val.child, {
                    parentMenuId: menu,
                    childOpenClass: childOpenClass,
                    leftMenuCheckDefault: leftMenuCheckDefault
                });
                headerMobileMenuHtml += me.compileMenu({
                    id: id,
                    menu: menu,
                    icon: val.icon,
                    title: val.title,
                }, true);
                headerMenuCheckDefault = "";
                leftMenuCheckDefault = "layui-hide";
                return topMenuItemHtml;
            }).join("");
            $('.layui-layout-body').addClass('layuimini-multi-module'); //多模块标识
            $('.layuimini-menu-header-pc').html(headerMenuHtml); //电脑
            $('.layuimini-menu-left').html(leftMenuHtml);
            $('.layuimini-menu-header-mobile').html(headerMobileMenuHtml); //手机
            element.init();
        },

        /**
         * 监听
         */
        listen: function () {
            /**
             * 菜单模块切换
             */
            $('body').on('click', '[data-menu]', function () {
                let loading = layer.load(0, {shade: false, time: 2 * 1000});
                let menuId = $(this).attr('data-menu');
                // header
                $(".layuimini-header-menu .layui-nav-item.layui-this").removeClass('layui-this');
                $(this).addClass('layui-this');
                // left
                $(".layuimini-menu-left .layui-nav.layui-nav-tree.layui-this").addClass('layui-hide');
                $(".layuimini-menu-left .layui-nav.layui-nav-tree.layui-this.layui-hide").removeClass('layui-this');
                $("#" + menuId).removeClass('layui-hide');
                $("#" + menuId).addClass('layui-this');
                layer.close(loading);
            });

            /**
             * 菜单缩放
             */
            $('body').on('click', '.layuimini-site-mobile', function () {
                let loading = layer.load(0, {shade: false, time: 2 * 1000});
                let isShow = $('.layuimini-tool [data-side-fold]').attr('data-side-fold');
                if (parseInt(isShow) === 1) { // 缩放
                    $('.layuimini-tool [data-side-fold]').attr('data-side-fold', 0);
                    $('.layuimini-tool [data-side-fold]').attr('class', 'layui-icon layui-icon-spread-left');
                    $('.layui-layout-body').removeClass('layuimini-all');
                    $('.layui-layout-body').addClass('layuimini-mini');
                } else { // 正常
                    $('.layuimini-tool [data-side-fold]').attr('data-side-fold', 1);
                    $('.layuimini-tool [data-side-fold]').attr('class', 'layui-icon layui-icon-shrink-right');
                    $('.layui-layout-body').removeClass('layuimini-mini');
                    $('.layui-layout-body').addClass('layuimini-all');
                    layer.close(window.openTips);
                }
                element.init();
                layer.close(loading);
            });
            /**
             * 菜单缩放
             */
            $('body').on('click', '[data-side-fold]', function () {
                let loading = layer.load(0, {shade: false, time: 2 * 1000});
                let isShow = $('.layuimini-tool [data-side-fold]').attr('data-side-fold');
                if (parseInt(isShow) === 1) { // 缩放
                    $('.layuimini-tool [data-side-fold]').attr('data-side-fold', 0);
                    $('.layuimini-tool [data-side-fold]').attr('class', 'layui-icon layui-icon-spread-left');
                    $('.layui-layout-body').removeClass('layuimini-all');
                    $('.layui-layout-body').addClass('layuimini-mini');

                } else { // 正常
                    $('.layuimini-tool [data-side-fold]').attr('data-side-fold', 1);
                    $('.layuimini-tool [data-side-fold]').attr('class', 'layui-icon layui-icon-shrink-right');
                    $('.layui-layout-body').removeClass('layuimini-mini');
                    $('.layui-layout-body').addClass('layuimini-all');
                    layer.close(window.openTips);
                }
                element.init();
                layer.close(loading);
            });

            /**
             * 手机端点开模块
             */
            $('body').on('click', '.layuimini-header-menu.layuimini-mobile-show dd', function () {
                let loading = layer.load(0, {shade: false, time: 2 * 1000});
                let check = $('.layuimini-tool [data-side-fold]').attr('data-side-fold');
                if (parseInt(check) === 1) {
                    $('.layuimini-site-mobile').trigger("click");
                    element.init();
                }
                layer.close(loading);
            });
        },

    };

    // 弹窗遮罩透明度配置
    let shadeConfig = [0.02, '#000'];

    let miniAdmin = {
        /**
         * 后台框架初始化
         * @param options.initUrl   后台初始化接口地址
         * @param options.clearUrl   后台清理缓存接口
         * @param options.urlHashLocation URL地址hash定位
         * @param options.multiModule 是否开启多模块
         * @param options.menuChildOpen 是否展开子菜单
         * @param options.loadingTime 初始化加载时间
         * @param options.pageAnim iframe窗口动画
         * @param options.maxTabNum 最大的tab打开数量
         */
        miniTab: miniTab,
        miniMenu: miniMenu,
        render: function (options) {
            options.initUrl = options.initUrl || null;
            options.urlHashLocation = options.urlHashLocation || false;
            options.multiModule = options.multiModule || false;
            options.menuChildOpen = options.menuChildOpen || false;
            options.loadingTime = options.loadingTime || 1;
            options.pageAnim = options.pageAnim || false;
            options.maxTabNum = options.maxTabNum || 20;
            $.getJSON(options.initUrl, function (data) {
                if (data == null) {
                    miniAdmin.error('暂无菜单信息');
                } else {
                    miniAdmin.renderLogo(data.logoInfo);
                    miniAdmin.renderHome(data.homeInfo);
                    miniAdmin.listen();
                    miniMenu.render({
                        menuList: data.menuInfo,
                        multiModule: options.multiModule,
                        menuChildOpen: options.menuChildOpen
                    });
                    miniTab.render({
                        filter: 'layuiminiTab',
                        urlHashLocation: options.urlHashLocation,
                        multiModule: options.multiModule,
                        menuChildOpen: options.menuChildOpen,
                        maxTabNum: options.maxTabNum,
                        menuList: data.menuInfo,
                        homeInfo: data.homeInfo,
                        listenSwitchCallback: function () {

                        }
                    });
                }
            }).fail(function () {
                miniAdmin.error('菜单接口有误');
            });
        },

        /**
         * 初始化logo
         * @param data
         */
        renderLogo: function (data) {
            let html = '<a href="' + data.href + '"><img src="' + data.image + '" alt="logo"><h1>' + data.title + '</h1></a>';
            $('.layuimini-logo').html(html);
        },

        /**
         * 初始化首页
         * @param data
         */
        renderHome: function (data) {
            sessionStorage.setItem('layuiminiHomeHref', data.href);
            $('#layuiminiHomeTabId').html('<span class="layuimini-tab-active"></span><span class="disable-close">' + data.title + '</span><i class="layui-icon layui-unselect layui-tab-close">ဆ</i>');
            $('#layuiminiHomeTabId').attr('lay-id', data.href);
            $('#layuiminiHomeTabIframe').html('<iframe width="100%" height="100%" border="0" frameborder="no" marginwidth="0" marginheight="0"  src="' + data.href + '"></iframe>');
        },

        /**
         * 成功
         * @param title
         * @returns {*}
         */
        success: function (title) {
            return layer.msg(title, {icon: 1, shade: shadeConfig, scrollbar: false, time: 2000, shadeClose: true});
        },

        /**
         * 失败
         * @param title
         * @returns {*}
         */
        error: function (title) {
            return layer.msg(title, {icon: 2, shade: shadeConfig, scrollbar: false, time: 3000, shadeClose: true});
        },

        /**
         * 监听
         */
        listen: function () {
            /**
             * 刷新
             */
            $('body').on('click', '[data-refresh]', function () {
                $(".layui-tab-item.layui-show").find("iframe")[0].contentWindow.location.reload();
                miniAdmin.success('刷新成功');
            });

            /**
             * 监听提示信息
             */
            $("body").on("mouseenter", ".layui-nav-tree .menu-li", function () {
                let tips = $(this).prop("innerHTML"),
                    isShow = $('.layuimini-tool i').attr('data-side-fold');
                if (parseInt(isShow) === 0 && tips) {
                    tips = '<ul class="layuimini-menu-left-zoom layui-nav layui-nav-tree layui-this"><li class="layui-nav-item layui-nav-itemed">' + tips + '</li></ul>';
                    window.openTips = layer.tips(tips, $(this), {
                        tips: [2, '#2f4056'],
                        time: 300000,
                        skin: "popup-tips",
                        success: function (el) {
                            let left = $(el).position().left - 10;
                            $(el).css({left: left});
                            element.render();
                        }
                    });
                }
            });

            $("body").on("mouseleave", ".popup-tips", function () {
                let isShow = $('.layuimini-tool i').attr('data-side-fold');
                if (parseInt(isShow) === 0) {
                    try {
                        layer.close(window.openTips);
                    } catch (e) {
                        console.log(e.message);
                    }
                }
            });
        }
    };

    exports("miniAdmin", miniAdmin);
});