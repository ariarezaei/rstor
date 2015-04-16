$(function() {
    console.log("Started this");
    ids = [
        'wr-ratio',
        'wr-throughput',
        'wr-response',
        'wr-request'
    ];

    modes = [
        'Hit Ratio',
        'Throughput',
        'Mean Response Time',
        'Mean Number of Requests'
    ];

    data = {};

    $.get("livestat", function(result){
        alert("DATA IS LOADED!");
        data = result;
        console.log(data);
    }, "json");

    for (i=0;i<4;i++)
    {
        draw_graph(ids[i], modes[i], data);
    }
});

function draw_graph(id, mode, data)
{
    // Creating a random graph with 2 lines for all 4 elements
    new Morris.Line({
        // Setting the element
        element: id,

        // Setting the data
        data: [
            {rank: '1', wr_res: Math.round(Math.random()*100), rd_res:Math.round(Math.random()*100)},
            {rank: '2', wr_res: Math.round(Math.random()*100), rd_res: Math.round(Math.random()*100)},
            {rank: '3', wr_res: Math.round(Math.random()*100), rd_res: Math.round(Math.random()*100)},
            {rank: '4', wr_res: Math.round(Math.random()*100), rd_res: Math.round(Math.random()*100)},
            {rank: '5', wr_res: Math.round(Math.random()*100), rd_res: Math.round(Math.random()*100)},
            {rank: '6', wr_res: Math.round(Math.random()*100), rd_res: Math.round(Math.random()*100)},
        ],

        // Setting x labels
        xkey: 'rank',

        // Setting y labels
        ykeys: ['wr_res', 'rd_res'],

        // Setting y label names
        labels: ['Write ' + mode, 'Read ' + mode],

        // options
        hideHover: 'auto'
    });

    //TODO: get the data using AJAX
}