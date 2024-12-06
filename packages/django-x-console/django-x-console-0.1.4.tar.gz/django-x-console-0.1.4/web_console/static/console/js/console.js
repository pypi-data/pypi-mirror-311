layui.config({
    base: '/static/console/js/',
}).extend({
    miniAdmin: 'miniAdmin',
});

var $ = layui.jquery,
    layer = layui.layer;

$('#moreFilter').on('click', function () {
    let moreFilter = $('.more-filter')
    let this_ = $(this)
    if (moreFilter.is(':hidden')) {
        moreFilter.css('display', 'inline-block')
        this_.html('收起<i class="layui-icon layui-icon-up"></i>')
    } else {
        moreFilter.css('display', 'none')
        this_.html('展开<i class="layui-icon layui-icon-down"></i>')
    }
})


function get_location_search() {
    return location.search
        .slice(1)
        .split('&')
        .map(p => p.split('='))
        .reduce((obj, pair) => {
            const [key, value] = pair.map(decodeURIComponent);
            obj[key] = value;
            return obj;
        }, {})
}