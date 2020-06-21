with rawdata as (SELECT id
  , ARRAY(
      SELECT JSON_EXTRACT_SCALAR(x, '$.name'),
      FROM UNNEST(JSON_EXTRACT_ARRAY(data, "$.results"))x
  ) name,
  ARRAY(
      SELECT JSON_EXTRACT_SCALAR(x, '$.business_status'),
      FROM UNNEST(JSON_EXTRACT_ARRAY(data, "$.results"))x
  ) business_status,
   ARRAY(
      SELECT JSON_EXTRACT_SCALAR(x, '$.formatted_address'),
      FROM UNNEST(JSON_EXTRACT_ARRAY(data, "$.results"))x
  ) formatted_address,
     ARRAY(
      SELECT JSON_EXTRACT_SCALAR(x, '$.rating'),
      FROM UNNEST(JSON_EXTRACT_ARRAY(data, "$.results"))x
  ) rating,
  
       ARRAY(
      SELECT JSON_EXTRACT_SCALAR(x, '$.user_ratings_total'),
      FROM UNNEST(JSON_EXTRACT_ARRAY(data, "$.results"))x
  ) user_ratings_total,
         ARRAY(
      SELECT JSON_EXTRACT_SCALAR(x, '$.geometry.location.lat'),
      FROM UNNEST(JSON_EXTRACT_ARRAY(data, "$.results"))x
  ) lat,
         ARRAY(
      SELECT JSON_EXTRACT_SCALAR(x, '$.geometry.location.lng'),
      FROM UNNEST(JSON_EXTRACT_ARRAY(data, "$.results"))x
  ) lng,
  ARRAY(
    SELECT array_to_string(JSON_EXTRACT_ARRAY(x, '$.types'),","),
      FROM UNNEST(JSON_EXTRACT_ARRAY(data, "$.results"))x
      ) types,
FROM `data-analytics-273208.bigdataproject.gmaps_parks_raw`)
SELECT id, name, business_status, formatted_address, rating, user_ratings_total, lat, lng, types  
FROM rawdata,
UNNEST(name) name WITH OFFSET pos0,
UNNEST(business_status) business_status WITH OFFSET pos1,
UNNEST(formatted_address) formatted_address WITH OFFSET pos2,
UNNEST(rating) rating WITH OFFSET pos3,
UNNEST(user_ratings_total) user_ratings_total WITH OFFSET pos4,
UNNEST(lat) lat WITH OFFSET pos5,
UNNEST(lng) lng WITH OFFSET pos6,
UNNEST(types) types WITH OFFSET pos7
WHERE pos0 = pos1 
and pos0 = pos2 
and pos0 = pos3 
and pos0 = pos4 
and pos0 = pos5 
and pos0 = pos6
and pos0 = pos7