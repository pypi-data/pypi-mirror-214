<%page args="projectMetadata, blueprints"/>
<!doctype html>
<html lang="en">
<%include
    file="ProjectWebsiteIndexHead.html.mako"
    args="projectMetadata=projectMetadata"/>
<body>

<!-- Project breadcrumbs -->
<nav aria-label="breadcrumb">
    <ol class="breadcrumb m-0">
        <li class="breadcrumb-item" aria-current="page">
            <a
                href="https://www.servertribe.com/"
                target="_blank">
                ServerTribe
            </a>
        </li>
        <li class="breadcrumb-item" aria-current="page">
            <a
                href="https://github.com/attune-Automation/"
                target="_blank">
                Attune Automation Projects
            </a>
        </li>
        <li class="breadcrumb-item active" aria-current="page">
            <strong>${projectMetadata.name}</strong>
        </li>
    </ol>
</nav>

<!-- Project Header -->
<%include
    file="ProjectWebsiteIndexHeader.html.mako"
    args="projectMetadata=projectMetadata"/>

<div class="documentation">
    <div class="container px-0">
        <div class="row">
            <!-- Documentation and Instruction Sets -->
<%include
    file="ProjectWebsiteIndexBlueprintsList.html.mako"
    args="blueprints=blueprints"/>
<%include
    file="ProjectWebsiteIndexAttuneAd.html.mako"/>
        </div>
<%include
    file="ProjectWebsiteIndexJoinDiscord.html.mako"/>
    </div>
</div>
<%include
    file="ProjectWebsiteIndexScripts.html.mako"/>
</body>
</html>
