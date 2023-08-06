<%page args="blueprint"/>

            <div class="col-lg-2 px-0 pr-5">
                <div class="container px-0 pt-3 sticky-top">
                    <h6 class="pb-2">
                        <strong>Contents</strong>
                    </h6>
                    <h6 class="text-muted">
                        <a href="#top">
                            <strong>${blueprint.name}</strong>
                        </a>
                    </h6>
<%include
    file="ProjectWebsiteBlueprintTocInner.html.mako"
    args="step=blueprint"/>
                </div>
            </div>