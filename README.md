# T.A.U.I-Train-And-Uber-Integration
___
<div style="text-align: center;">
    <img src="cats_on_mars.png" width="200" />
</div>

#### A project to integrate Uber and Train services in a single web application.
Taui aims to provide a seamless experience for users who wish to use both Uber and Train services to get to their destination. The user will be able to enter their starting location and destination, and Taui will find the nearest train station to the starting location, as well as the nearest train station to the destination. Taui will then find the ideal route to take, factoring in the nearest train stations, and the time it takes to get to the train stations. Taui will then provide the user with a link to book an Uber to the nearest train station, and a link to book an Uber from the destination train station to the final destination. This will allow the user to book both their initial ride, and final ride with ease. 


* We are using a mixture of Python with the Flask library for the backend as well as HTML, CSS, and JavaScript for the frontend.
* We are using the Google Maps API to display the map and find the ideal route factoring in the nearest train stops.
* We are using Uber Deeplinks to redirect the user to the Uber app with the destination already set, allowing them to book both of their rides with ease.

### How to use T.A.U.I

---
1. Go to https://taui.pythonanywhere.com/
2. Input your starting location and destination
3. Click the "Get Route" button
4. Click the "Book Uber" button to book your Uber to the nearest train station
5. Click the arrow button to move on to the next map and see your train route
6. Click the arrow button again to move on to the final map and see your Uber route from the destination train station to your final destination
7. Enjoy your ride!

### Common Errors

---
* Sometimes when you input the name of a location, the map will not display the location. 
This is because the Google Maps API does not recognize the location you entered. 
To fix this, try entering a more specific location, or try entering the address of the location.
### Contributors

---
* Angelo L. [GitHub](https://github.com/SatisfiedSushi)  
Junior at Northside College Prep, I am the lead programmer of the robotics team and I enjoy kayaking and playing guitar in my free time.
* Aditya G. [GitHub](https://github.com/agaur12)  
Junior at Northside College Prep, I am the PR Director of the robotics team and I enjoy playing soccer.
* Alex D. [GitHub](https://github.com/AlexD2112)  
Junior at Northside College Prep,I program for the robotics team. In my free time, I play guitar and go biking. 
* Michael M. [GitHub](https://github.com/ThatOneGuy631)  
Senior at Northside college prep, I am the captain of the robotics team
and I enjoy playing saxophone and the bass guitar in my free time.

## License
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.