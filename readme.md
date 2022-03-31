This is a very simple tool for assisting observe the diff result.

### How to use
1. This tool would look at projects inside the `observed_projects` folder. And show all projects' diff for the newest 50 commits. The project need to exist `.gitattribute`, which contain `*.js diff=javascript` like setting.
2. Modidy `gitBinPath` variable into your git binary path.
3. After executing `main.py`, the diff_result directory will contain <XXX>_content.txt and <XXX>_result.diff. Ex:
    has jquery_content.txt, below is one diff's result in jquery_content.txt
    ```text
    diff --git a/a.js b/b.js
    @@ -22,7 +22,6 @@ module.exports = function( grunt ) {
    A blob:687b3215c92928c5ca3714822497b490d264af9f
    "use strict";

    module.exports = function( grunt ) {
        function readOptionalJSON( filepath ) {
            var stripJSONComments = require( "strip-json-comments" ),
                data = {};
            try {
                data = JSON.parse( stripJSONComments(
                    fs.readFileSync( filepath, { encoding: "utf8" } )
                ) );
            } catch ( e ) {}
            return data;
        }

        // Support: Node.js <12
        // Skip running tasks that dropped support for Node.js 10
        // in this Node version.
        function runIfNewNode( task ) {
            return oldNode ? "print_old_node_message:" + task : task;
        }

        var fs = require( "fs" ),
            gzip = require( "gzip-js" ),
            oldNode = /^v10\./.test( process.version ),
            nodeV17OrNewer = !/^v1[0246]\./.test( process.version ),
            isCi = process.env.GITHUB_ACTION,
            ciBrowsers = process.env.BROWSERS && process.env.BROWSERS.split( "," );

        if ( !grunt.option( "filename" ) ) {
    ```

    has jquery_result.diff, below is one diff's result in jquery_result.diff
    ```diff
    diff --git a/a.js b/b.js
    index 687b3215..7514c9a7 100644
    --- a/a.js
    +++ b/b.js
    @@ -22,7 +22,6 @@ module.exports = function( grunt ) {
        var fs = require( "fs" ),
            gzip = require( "gzip-js" ),
            oldNode = /^v10\./.test( process.version ),
    -		nodeV17OrNewer = !/^v1[0246]\./.test( process.version ),
            isCi = process.env.GITHUB_ACTION,
            ciBrowsers = process.env.BROWSERS && process.env.BROWSERS.split( "," );
    ```
    We can observe the diff change in `jquery_result.diff`, and the `jquery_content.txt` can show more content, including the code reaching the hunk header and a few lines above the hunk header. So we can judge header is correct or unsuitable.