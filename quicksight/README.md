# QuickSight notes

1. Ensure QuickSight has permissions to use Athena and the S3 query results bucket.
2. In QuickSight: Manage Data -> New dataset -> Choose Athena -> select the Glue database/table.
3. Choose Direct Query (or import to SPICE), then build visuals:
   - KPI card: Top artist by album count
   - Bar chart: Top tracks by popularity
   - Line chart: Releases over time
