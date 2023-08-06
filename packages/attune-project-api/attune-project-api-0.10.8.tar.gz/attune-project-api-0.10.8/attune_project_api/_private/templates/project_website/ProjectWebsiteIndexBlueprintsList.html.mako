<%page args="blueprints"/>
            <div class="col-lg-10 mt-3 px-0">
                <div class="container">
                    <div class="row">
                        <div class="col pl-0">
                            <h6>
                                This project contains the following
                                documentation and instruction sets:
                            </h6>
                        </div>
                    </div>

                    <!-- Blueprints listed with names and descriptions -->
                    <div class="row">
% for blueprint in blueprints:
                        <div class="col-12 pt-3 pl-0">
                            <div class="card"
                                 id="${blueprint.key}">
                                <div class="card-body">
                                    <a href="blueprints/${blueprint.key}.html">
                                        <h3 class="card-title">
                                            ${blueprint.name}
                                        </h3>
                                    </a>
% if blueprint.comment:
                                    <p class="card-text">
                                        ${blueprint.makeCommentHtml(4)}
                                    </p>
% endif
                                </div>
                            </div>
                        </div>
% endfor
                    </div>
                </div>
            </div>