SELECT title
FROM people
JOIN stars on stars.person_id = people.id
JOIN movies ON stars.movie_id = movies.id
WHERE name = "Johnny Depp"
AND movie_id in (
    SELECT movie_id
    FROM people JOIN stars ON stars.person_id = people.id
    WHERE name = 'Helena Bonham Carter'
);
