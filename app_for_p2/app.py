# Import Dependencies
from flask import (Flask, render_template, jsonify, request)
import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base

# Set up flask
app = Flask(__name__)

# Initiate datebase session
engine = create_engine('sqlite:///data/unified_db.sqlite')
print('Connected to DB')
Base = automap_base()
Base.prepare(engine, reflect=True)
session = Session(engine)
Posts = Base.classes.posts

# Flask routes
@app.route("/")
def home():
    return render_template('index.html')

@app.route("/hashtag_vs_interaction")
def hashtag_vs_interactions_page():
    return render_template('hashVSlikes.html')

@app.route("/hashtag_vs_interaction/<account_selected>")
def hashtag_vs_interactions_data(account_selected):
    hashtags_vs_int_list = []

    # One set of data for each post type
    for type_selected in ['photo', 'video', 'album']:
        
        # Query the data decided by user selection
        type_query = session.query(Posts).filter_by(post_type=f'{type_selected}')

        if account_selected == 'all':
            account_query = type_query
        else:
            account_query = type_query.filter_by(account_name=f'{account_selected}')
        
        # Format the data from query
        hashtag_counts = [post.hashtag_count for post in account_query.all()]
        follower_counts = [post.account_follower_count for post in account_query.all()]

        # Format the data from query
        hashtag_counts = [post.hashtag_count for post in account_query.all()]
        follower_counts = [post.account_follower_count for post in account_query.all()]

        # Use interaction_count for both likes and views
        interaction_counts_list = []
        for post in account_query.all():
            interaction_count = post.view_count
            if interaction_count == None:
                interaction_count = post.like_count
            interaction_counts_list.append(interaction_count)

        # Calculate interaction per follower
        interaction_per_follower_list = [
            interaction_counts_list[i]/follower_counts[i] \
            for i in range(0, len(account_query.all()))
        ]
        
        # Aggregate data for plotting
        intermediate_df = pd.DataFrame({
            'hashtag_count': hashtag_counts,
            'interaction_per_follower': interaction_per_follower_list
        })

        to_plot_df = intermediate_df.groupby('hashtag_count').mean()
        to_plot_df.rename(columns={'interaction_per_follower': 'avg_interactions_per_follower'}, inplace=True)
        to_plot_df['post_count'] = intermediate_df.groupby('hashtag_count').count()
        
        # Save the data in for js retrieval
        to_plot_dict = {
            'post_type': type_selected,
            'hashtag_count': list(map(int, to_plot_df.index.tolist())),
            'int_per_follower': list(map(float, to_plot_df.avg_interactions_per_follower.tolist())),
            'post_count': list(map(int, to_plot_df.post_count.tolist()))
        }

        hashtags_vs_int_list.append(to_plot_dict)

    return jsonify(hashtags_vs_int_list)

if __name__ == "__main__":
    app.run(debug=True, port=5005)