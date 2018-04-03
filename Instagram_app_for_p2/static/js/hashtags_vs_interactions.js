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
    Plotly.d3.json(`/hashtag_vs_interaction/${account_selected}`, function(error, plotData){
        if (error) return console.warn(error);
        
        var photosData = plotData[0];
        var videosData = plotData[1];
        var albumsData = plotData[2];

        // Make chart for photo-type posts
        var trace1 = {
            x: photosData.hashtag_count,
            y: photosData.int_per_follower,
            fill: 'tozeroy',
            type: 'scatter',
            name: 'Likes per Follower'
        };

        var trace2 = {
            x: photosData.hashtag_count,
            y: photosData.post_count,
            fill: 'tonexty',
            type: 'scatter',
            name: 'Number of Posts',
            yaxis: 'y2'
        }
        
        var data = [trace1, trace2];

        var layout = {
            title: `Photo posts by ${account_selected}`,
            xaxis: {
                title: 'Number of Hashtags Used in Caption',
                rangemode: 'tozero'
            },
            yaxis: {
                title: 'Average Likes per Photo per Follower',
                rangemode: 'tozero'
            },
            yaxis2: {
                title: 'Number of Photo Posts',
                overlaying: 'y',
                side: 'right',
                rangemode: 'tozero'
            },
            legend: {
                x: 0,
                y: -50
            }
        };

        Plotly.newPlot('photosChart', data, layout)

        // Make chart for video-type posts
        var trace1 = {
            x: videosData.hashtag_count,
            y: videosData.int_per_follower,
            fill: 'tozeroy',
            type: 'scatter',
            name: 'Views per Follower'
        };

        var trace2 = {
            x: videosData.hashtag_count,
            y: videosData.post_count,
            fill: 'tonexty',
            type: 'scatter',
            name: 'Number of Posts',
            yaxis: 'y2'
        }
        
        var data = [trace1, trace2];

        var layout = {
            title: `Video posts by ${account_selected}`,
            xaxis: {
                title: 'Number of Hashtags Used in Caption',
                rangemode: 'tozero'
            },
            yaxis: {
                title: 'Average Views per Video per Follower',
                rangemode: 'tozero'
            },
            yaxis2: {
                title: 'Number of Video Posts',
                overlaying: 'y',
                side: 'right',
                rangemode: 'tozero'
            },
            legend: {
                x: 0,
                y: -50
            }
        };

        Plotly.newPlot('videosChart', data, layout)

        // Make chart for album-type posts
        var trace1 = {
            x: albumsData.hashtag_count,
            y: albumsData.int_per_follower,
            fill: 'tozeroy',
            type: 'scatter',
            name: 'Likes per Follower'
        };

        var trace2 = {
            x: albumsData.hashtag_count,
            y: albumsData.post_count,
            fill: 'tonexty',
            type: 'scatter',
            name: 'Number of Posts',
            yaxis: 'y2'
        }
        
        var data = [trace1, trace2];

        var layout = {
            title: `Album posts by ${account_selected}`,
            xaxis: {
                title: 'Number of Hashtags Used in Caption',
                rangemode: 'tozero'
            },
            yaxis: {
                title: 'Average Likes per Album per Follower',
                rangemode: 'tozero'
            },
            yaxis2: {
                title: 'Number of Album Posts',
                overlaying: 'y',
                side: 'right',
                rangemode: 'tozero'
            },
            legend: {
                x: 0,
                y: -50
            }
        };

        Plotly.newPlot('albumsChart', data, layout)


    })
}

// Make this the default
optionChanged('all')