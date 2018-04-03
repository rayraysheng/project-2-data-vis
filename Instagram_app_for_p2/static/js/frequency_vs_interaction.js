// Fetch data
Plotly.d3.json('/frequency_vs_interaction_get_data', function(error, plotData){
    if (error) return console.warn(error);

    var colors = [
        '#F27370',
        '23B1A5',
        'FA4659',
        'FFDD7E',
        '0081C6',
        '8559A5',
        '4C6F7B',
        'FF6D24',
        '00BBF0',
        '7E6752'
    ]

    var postFrequency = plotData.post_per_day;
    var sizeValues = [plotData.follower_count.map(x => x/100000)][0];
    console.log(sizeValues);
    var accountNames = plotData.account_name;

    // Load chart
    optionChanged = function(typeSelected){
        if (typeSelected == 'likes') {
            var traceLikes = {
                x: postFrequency,
                y: plotData.like_per_follower,
                text: accountNames,
                mode: 'markers',
                marker: {
                    size: sizeValues,
                    color: colors
                }
            };

            var data = [traceLikes];

            var layout = {
                title: 'Post Frequency vs. Phot & Album Likes',
                xaxis: {
                    title: 'Posts per Day',
                    rangemode: 'tozero'
                },
                yaxis: {
                    title: 'Like per Follower',
                    rangemode: 'nonnegative'
                }
            }

            Plotly.newPlot('chartArea', data, layout)
        } 
        
        else if (typeSelected == 'views') {
            var traceLikes = {
                x: postFrequency,
                y: plotData.view_per_follower,
                text: accountNames,
                mode: 'markers',
                marker: {
                    size: sizeValues,
                    color: colors
                }
            };

            var data = [traceLikes];

            var layout = {
                title: 'Post Frequency vs. Video Likes',
                xaxis: {
                    title: 'Posts per Day',
                    rangemode: 'tozero'
                },
                yaxis: {
                    title: 'View per Follower',
                    rangemode: 'nonnegative'
                }
            }

            Plotly.newPlot('chartArea', data, layout)
        }

        else {
            var traceLikes = {
                x: postFrequency,
                y: plotData.int_per_follower,
                text: accountNames,
                mode: 'markers',
                marker: {
                    size: sizeValues,
                    color: colors
                }
            };

            var data = [traceLikes];

            var layout = {
                title: 'Post Frequency vs. Likes & Views',
                xaxis: {
                    title: 'Posts per Day',
                    rangemode: 'tozero'
                },
                yaxis: {
                    title: 'Like or View per Follower',
                    rangemode: 'nonnegative'
                }
            }

            Plotly.newPlot('chartArea', data, layout)
        }
    }

    // Make this the default
    optionChanged('all')
})

