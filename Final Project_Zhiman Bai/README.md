===Christmas Movies Visualization===

===Concept Description===
As the holiday season approaches, this project visualizes Christmas movie data from 1934 to 2023, using interactive Christmas trees as a playful medium.
Each tree represents one year, and its height corresponds to the average IMDb rating of movies released that year. 
Each colored bulb represents an individual movie, with colors showing content ratings.

===Features===
1. Tree Visualization: Each tree corresponds to a year and scales in height according to the average IMDb rating of movies for that year.
2. Bulbs: Represent individual movies on the tree. 
3. Color-coded based on movie rating: 
   G: Green, 
   PG: Yellow, 
   PG-13: Orange, 
   R: Red, 
   Not Rated/others: Gray.
4. Interactive Slider: Navigate through different years by dragging the slider.
5. Legend: Explains what each visual element represents.

===Data Source===
This dataset was sourced from IMDb. (I found online.)

The project used the CSV file "christmas_movies.csv" with the following columns:
title: Movie title
release_year: Year the movie was released
imdb_rating: IMDb rating of the movie
rating: Content rating (G, PG, PG-13, R, etc.)

(The CSV file is located in the same directory as the main script.)

===Mapping Strategy===
Tree height is scaled according to the average IMDb rating of movies released in that year.  
Bulbs are placed randomly within the tree shape and colored according to their rating category.  

===Instructions to Run the Code===
Make sure the following files are in the same directory:
1. BAI_data_art.py (main loop of visualization)
2. visual_objects.py (classes)
3. christmas_movies.csv (dataset)
4. background.jpg (background image)

Controls: Drag the slider to navigate through different years. Trees and bulbs update dynamically as the slider moves.

===Screenshots are included in the project folder===