var graphsInterval;

var hitRatioGraph;
var throughputGraph;
var responseGraph;
var requestGraph;

hitRatioData = [];
throughputData = [];
responseData = [];
requestData = [];

var globalTime;

$(function() {
    console.log("Initiated the charts");

    hitRatioGraph = start_graph("wr-ratio", "Hit Ratio");
    throughputGraph = start_graph("wr-throughput", "Throughput");
    responseGraph = start_graph("wr-response", "Mean Response Time");
    requestGraph = start_graph("wr-request", "Mean Number of Requests");

    graphsInterval = window.setInterval(update_charts, 1000);

    globalTime = 1;

});


function add_point(first, second, time, graph, data) {

    data.push({
        'time': time+"s",
        'wr_res': first,
        'rd_res': second
    });

    graph.setData(data);
}

function update_charts()
{
    console.log("Update started");
    $.get("livestat", function(result){
        console.log("Data is loaded, result = ");
        data = result;
        console.log(data);
        // Hit Ratio. Note: YOU SHOULD FIRST PASS THE 'WRITE' NUMBER THROUGH
        add_point(
            data['write_hit_rate'],
            data['read_hit_rate'],
            globalTime,
            hitRatioGraph,
            hitRatioData
        );

        // Throughput
        add_point(
            data['throughput_write'],
            data['throughput_read'],
            globalTime,
            throughputGraph,
            throughputData
        );

        // Response Time
        add_point(
            data['write_mean_response'],
            data['read_mean_response'],
            globalTime,
            responseGraph,
            responseData
        );

        // Request Number
        add_point(
            data['writes'],
            data['reads'],
            globalTime,
            requestGraph,
            requestData
        );

    }, "json");

    globalTime += 1;
}

function start_graph(id, mode)
{
    return Morris.Line({
        element: id,

        data: [],

        xkey: 'time',
        ykeys: ['wr_res', 'rd_res'],
        labels: ['Write + ' + mode, 'Read ' + mode],

        hideHover: 'auto',

        smooth: 'false'
    });
}