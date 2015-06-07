var isLoading = false;





// Initial function
$(function() {
    //console.log("Initiated the charts");

    $('#start-time-picker').datetimepicker();
    $('#end-time-picker').datetimepicker();

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

function send_info()
{
    sending_data = {
        cache_name: $('#cache-name').val(),
        start_date: $('#starting-date').val(),
        end_date: $('#ending-date').val()
    };

    $.post("", sending_data)
        .done(function(data){
            turnOffLoading();

            set_chart_data(
                'wr-throughput',
                data['w-throughput'],
                data['r-throughput']
            );
            set_chart_data(
                'wr-ratio',
                data['w-hitratio'],
                data['r-hitratio']
            );
            set_chart_data(
                'wr-response',
                data['w-response'],
                data['r-response']
            );
            set_chart_data(
                'wr-request',
                data['w-request'],
                data['r-request']
            );
        })
        .fail(function(){
            alert('Something went wrong. Please try again later.');
        })
        .always(function(){
    });
}

function clear_fields()
{
    $('#cache-name').val("Please choose a cache");
    $('#starting-date').val("");
    $('#ending-date').val("");
}

function set_chart_data(chart_name, write_data, read_data)
{
    var chart = $('#' + chart_name).highcharts();

    chart.series[0].setData(write_data);
    chart.series[1].setData(read_data);

    chart.redraw();
}