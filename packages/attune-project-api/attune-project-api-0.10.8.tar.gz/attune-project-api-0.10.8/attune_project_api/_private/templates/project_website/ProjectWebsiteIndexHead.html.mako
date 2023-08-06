<%page args="projectMetadata"/>
<%
    description = (projectMetadata.comment[0:300] if projectMetadata.comment else '')
%>
<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="title"
          content="Attune Automation Projects: ${projectMetadata.name}">
    <meta name="description"
          content="${description}">
    <meta name="robots"
          content="follow, index, max-snippet:-1, max-video-preview:-1, max-image-preview:large">

    <meta property="og:locale" content="en_AU"/>
    <meta property="og:type" content="article"/>
    <meta property="og:title"
          content="Attune Automation Projects: ${projectMetadata.name}"/>
    <meta property="og:description" content="${description}"/>
    <meta property="og:site_name" content="Attune Automation"/>
    <meta property="article:section" content="IT Instruction"/>

    <meta name="twitter:title"
          content="Attune Automation Projects: ${projectMetadata.name}"/>
    <meta name="twitter:description" content="${description}"/>

    <link rel="stylesheet"
          href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css"
          integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
          crossorigin="anonymous">
    <link rel="stylesheet" href="styles/style.css">

    <title>Attune Project: ${projectMetadata.name}</title>
</head>