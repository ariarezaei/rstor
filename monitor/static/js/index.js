// The time between two updates
var T = 5;
// The number of data points in a chart
var N = 30;
// Current update handler
var updateHandler = undefined;
var isLoading = false;
var names = ["wr-ratio", "wr-throughput", "wr-response", "wr-request"];

// Initial function
$(function() {
    //console.log("Initiated the charts");

    Highcharts.setOptions({
        lang:{
            loading: "Please select a cache."
        }
    });

    create_graph(
        'wr-ratio',
        'Read & Write Hit Ratio',
        'Hit Ratio (%)',
        'Hit Ratio'
    );

    create_graph(
        'wr-throughput',
        'Read & Write Throughput',
        'Throughput (IO/s)',
        'Throughput'
    );

    create_graph(
        'wr-response',
        'Read & Write Response Time',
        'Response Time (ms)',
        'Response Time'
    );

    create_graph(
        'wr-request',
        'Read & Write Request Rate',
        'Mean Request Rate',
        'Request Rate'
    );

    //update_charts();
    toggleLoading();

    //graphsInterval = window.setInterval(update_charts, T * 1000);
});

// Toggles loading status
function toggleLoading()
{
    if (isLoading == false)
    {
        $('[data-type="chart"]').each(function(){
            $(this).highcharts().showLoading();
        });
        isLoading = true;
    }
    else
    {
        $('[data-type="chart"]').each(function(){
            $(this).highcharts().hideLoading();
        });
        isLoading = false;
    }
}

// Turns off loading status
function turnOffLoading()
{
    $('[data-type="chart"]').each(function(){
        $(this).highcharts().hideLoading();
    });
    isLoading = false;
}

// Creates an empty chart
function create_graph(id, title, ytitle, mode)
{
    $('#' + id).highcharts({
        chart: {
            type: 'areaspline'
        },

        title: {
            text: title
        },

        loading: {
            style: {
              'font-size': '3em'
            },
            labelStyle: {
                top: '35%'
            }
        },

        xAxis: {
            type: 'datetime',
            tickPixelInterval: 150
        },

        yAxis: {
            title: {
                text: ytitle
            },

            min: function(){
                if (mode == "Hit Ratio")
                {
                    return 0;
                }
                return undefined;
            }(),
            max: function(){
                if (mode == "Hit Ratio")
                {
                    return 100;
                }
                return undefined;
            }(),
            tickInterval: 10
        },

        credits: {
            enabled: false
        },

        legend: {
            align: 'center'
        },

        exporting: {
            enabled: false
        },

        tooltip: {
            formatter: function () {
                return Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' +
                    '<b>' + this.points[0].series.name + '</b>: ' + Highcharts.numberFormat(this.points[0].y, 2) + '<br/>' +
                    '<b>' + this.points[1].series.name + '</b>: ' + Highcharts.numberFormat(this.points[1].y, 2);
            },
            shared: true
        },

        plotOptions: {
            spline: {
                animation: false
            }
        },

        series: [{
            name: 'Read ' + mode
        }, {
            name: 'Write' + mode
        }]
    });
}

// Initializes a chart with NUM points of zero
function init(num)
{
    var dataWrite = [],
        dataRead = [];

    for (var i=num*(-1);i<0;i++)
    {
        dataWrite.push({
            x: (new Date()).getTime() + i * T * 1000,
            y: 0
        });

        dataRead.push({
            x: (new Date()).getTime() + i * T * 1000,
            y: 0
        });
    }

    for (i=0;i<names.length;i++)
    {
        console.log("Initializing " + names[i]);
        var chart = $('#' + names[i]).highcharts();
        chart.series[0].setData(dataWrite);
        chart.series[1].setData(dataRead);

        chart.redraw();
    }
}

// Loads cache information when a cache is selected
function load_cache_info(cache_name)
{
    $.get( "config/" + cache_name, function(result){
        console.log("Succesfully acquired cache info");
        console.log(result);
        $("#main_disk_name").html(result['main_disk_name']);
        $("#main_disk_size").html(result['main_disk_size']);

        $("#cache_disk_name").html(result['cache_disk_name']);
        $("#cache_state").html(result['cache_state']);
        $("#cache_type").html(result['cache_type']);
        $("#cache_size").html(result['cache_size']);
        $("#block_size").html(result['block_size']);
    }, "json");
}

// Starts updates after a cache is selected
function start_updates(interval)
{
    var cache_name = $('#cache-name').val();
    if (cache_name == "Please choose a cache")  return;
    load_cache_info(cache_name);
    // Turning off
    clearInterval(updateHandler);

    // Stop loading
    turnOffLoading();

    // Initialize
    init(N);
    update_charts(); // This is the first points as user selects a cache

    // Set update intervals
    updateHandler = window.setInterval(update_charts, T * 1000);
}

// Adds a set of points to a given chart
function add_point(write, read, id)
{
    // read comes first
    // write comes second

    var chart = $('#' + id).highcharts();
    var curTime = new Date().getTime();
    chart.series[0].addPoint([curTime, read], false, true);
    chart.series[1].addPoint([curTime, write], true, true);
}

// Updates all the charts
function update_charts()
{
    var cache_name = $('#cache-name').val();
    //console.log("Update started");
    $.get("livestat/" + cache_name , function(result){
        //console.log("Data is loaded, result = ");
        data = result;
        //console.log(data);
        // Hit Ratio. Note: YOU SHOULD FIRST PASS THE 'WRITE' NUMBER THROUGH
        add_point(
            data['write_hit_rate'],
            data['read_hit_rate'],
            'wr-ratio'
        );

        // Throughput
        add_point(
            data['throughput_write'],
            data['throughput_read'],
            'wr-throughput'
        );

        // Response Time
        add_point(
            data['write_mean_response'],
            data['read_mean_response'],
            'wr-response'
        );

        // Request Number
        add_point(
            data['writes'],
            data['reads'],
            'wr-request'
        );

    }, "json");
}