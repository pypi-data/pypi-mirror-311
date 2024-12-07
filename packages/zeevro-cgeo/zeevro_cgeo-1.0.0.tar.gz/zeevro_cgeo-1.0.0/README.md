# zeevro-cgeo
A python C module with geographic functions

This library has two functions:

* `great_circle_distance(s_lat, s_lng, d_lat, d_lng)`: Returns the distance between two coordinates on earth
* `point_inside_polygon(px, py, ((x1, y1), (x2, y2), ...))`: Returns `True` or `False` depending on whether the point [px, py] is inside the polygon given by [[x1, y1], [x2, xy], ...]
