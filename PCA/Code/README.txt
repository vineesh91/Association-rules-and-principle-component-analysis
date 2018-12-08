RUNNING THE CODE

Change the value of the variable "file_name" with the file (data) to be explored.
Variable "choose_method" has 3 values
If equal to 1, then basic eigen method is executed.
If equal to 2, then svd method is executed.
If equal to 3, then t-sne method is executed.

To visualize svd for non mean-cenetered data, comment the svd function call with the norm_data and uncomment the svd function call with feature data inside the eigen_svd_main funciton. In the same function, please comment the line y = norm_data.dot(new_dim) and uncomment the line y = features.dot(new_dim).