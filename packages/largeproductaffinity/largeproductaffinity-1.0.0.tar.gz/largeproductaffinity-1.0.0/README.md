# large_product_affinity
large_product_affinity is used to obtain Product Affinity using big data without PySpark environment

Features:
1. large_product_affinity has been proven to handle millions of rows of transactional data
2. It can also handle tens of thousands of products
3. large_product_affinity requires only a dataframe with just two columns
4. It requires minimal pre-processing
5. No post-processing required

Requirements for Input data:
1. Data should be in a dataframe format of two columns
2. First column must be transaction id or any field containing transaction information
3. Second column should be products corresponding to transactions in the first column

Input:
1. Please, Choose an acceptable Support

Pre-Processing:
1. No Nulls

Post-Processing:
None

Output:
1. Product Affinity table is sorted in the order of Confidence and Lift in descending order.

Drawbacks:
1. The only drawback noted was the user's system capability to read data.
2. Please, Use Modin or Dask to read large volumes of data if Pandas fails.
