# Visitor analytics

Cloudflare Web Analytics uses the site's public beacon token. The loader runs
only on antoineboucher.info and www.antoineboucher.info and checks for an existing
beacon to avoid duplicating one injected by Cloudflare. Local previews do not
report visits. Keep the About generator and Hugo partial aligned with CV HTML.

The CV visitor map uses the owner's supplied MapMyVisitors image embed and links
to https://mapmyvisitors.com/web/1c8zo. It loads only when expanded, so its counts
reflect widget requests, not every page view. Cloudflare independently collects
site-wide analytics. The existing clustrmaps CSS/DOM names are retained for
compatibility; the runtime no longer requests ClustrMaps.

Live Cloudflare totals cannot be read with the public beacon token. A future
server-side integration needs an account ID and a scoped analytics-read API token
stored as a deployment secret, then a cached endpoint that publishes only chosen
aggregate metrics. Never put that API token in HTML or browser JavaScript.
The pasted dashboard's 9 visits / 9 page views was a last-24-hours snapshot, not a
live feed; it is deliberately not presented as a current public counter.

References:
- https://developers.cloudflare.com/web-analytics/data-metrics/data-origin-and-collection/
- https://developers.cloudflare.com/analytics/graphql-api/
