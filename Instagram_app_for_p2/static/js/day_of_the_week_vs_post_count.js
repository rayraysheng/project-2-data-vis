// Populate the dropdown menu

var accountsArr = [
    'aliceandolivia',
    'bananarepublic',
    'burberry',
    'chloe',
    'coach',
    'ferragamo',
    'gucci',
    'majeofficiel',
    'michaelkors',
    'toryburch'
];

var brandsArr = [
    'Alice and Olivia',
    'Banana Republic',
    'Burberry',
    'Chloe',
    'Coach',
    'Ferragamo',
    'Gucci',
    'Maje',
    'Michael Kors',
    'Tory Burch'
];

// Create the all brands option
var optionAll = document.createElement('option');
optionAll.text = 'All Brands';
optionAll.value = 'all';
optionAll.selected;

document.getElementById('selAccount').appendChild(optionAll)

// Loop through all the account names
for (i = 0; i < accountsArr.length; i++){
        
    // Create an option for each name
    var optionEl = document.createElement('option');
    optionEl.text = brandsArr[i];
    optionEl.value = accountsArr[i];
    
    // Add the option to the dropdown
    var selectEl = document.getElementById('selAccount');
    selectEl.appendChild(optionEl);
}  

optionChanged = function(account_selected){
    
    // Fetch data to plot
    Plotly.d3.json(`/day_of_the_week_vs_post_count/${account_selected}`, function(error, plotData){
        if (error) return console.warn(error);
        
        var weekdayLabels = [
            'Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday',
            'Saturday',
            'Sunday'
        ]


        // Make chart for Posts
        var traceLikePosts = {
            x: weekdayLabels,
            y: plotData.like_post_count,
            type: 'bar',
            name: 'Photos & Albums'
        };

        var traceViewPosts = {
            x: weekdayLabels,
            y: plotData.view_post_count,
            type: 'bar',
            name: 'Videos',
        }
        
        var data = [traceLikePosts, traceViewPosts];

        var layout = {
            title: `Posts by ${account_selected}`,
            barmode: 'stack'
        };

        Plotly.newPlot('allChart', data, layout);

        // Make chart for Total Likes & Views
        var traceTotLikes = {
            x: weekdayLabels,
            y: plotData.total_likes,
            type: 'bar',
            name: 'Photos & Albums'
        };

        var traceTotViews = {
            x: weekdayLabels,
            y: plotData.total_views,
            type: 'bar',
            name: 'Videos',
        }
        
        var data = [traceTotLikes, traceTotViews];

        var layout = {
            title: `Total Likes & Views for ${account_selected}`,
            barmode: 'stack'
        };

        Plotly.newPlot('totLikesViewsChart', data, layout);

        // Make chart for Average Likes & Views
        var traceAvgLikes = {
            x: weekdayLabels,
            y: plotData.avg_likes,
            type: 'bar',
            name: 'Photos & Albums'
        };

        var traceAvgViews = {
            x: weekdayLabels,
            y: plotData.avg_views,
            type: 'bar',
            name: 'Videos',
        }
        
        var data = [traceAvgLikes, traceAvgViews];

        var layout = {
            title: `Average Likes & Views for ${account_selected}`,
            barmode: 'stack'
        };

        Plotly.newPlot('avgLikesViewsChart', data, layout)
    })
}

// Make this the default
optionChanged('all')