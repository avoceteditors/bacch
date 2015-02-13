<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
    version="2.0"
    xmlns:xi="http://www.w3.org/TR/xinclude/">

<xsl:template match="book">
  <html>
    <head>

      <style type="text/css">
	div.main {}
	div.primary {
	   margin-bottom: 2.5em;
	   margin-top: 2.5em;
	}

	ul.barlist li {
	   float:left;
	   list-style-type: none;
	   padding-right: 1em;
	   font-weight:bold;
	   font-size:10pt;
	   font-family:Arial;
	}
	ul.barlist {
	   display: block;
	   padding:1em;
	   text-align:center;
	}

	div.primary,
	div.secondary {
	   text-align: justify;
	   font-family: Times;
	   }

	p.para1 {
	   text-indent: 0;
	}
	p {
	   text-indent: 2em;
	   line-height:1.1;
	   -webkit-margin-before:0.25em;
	   -webkit-margin-after:0.25em;
	}

      </style>

    </head>
    <body>
      <div class="heading">
	<h1><xsl:value-of select="info/title"/></h1>
	<p><xsl:value-of select="info/author"/></p>
      </div>
      <div class="main">
	<xsl:apply-templates/>
      </div>
    </body>
  </html>
</xsl:template>




<xsl:template match="chapter | preface">
  <div class="chapter">
    <h2><xsl:value-of select="title"/></h2>

    <ul class="barlist">
    <xsl:for-each select="section/title | section/section/title">
      <li><xsl:apply-templates/></li>  
    </xsl:for-each>
    </ul>

  <xsl:apply-templates/>
  </div>
</xsl:template>




<xsl:template match="title | info"/>

<xsl:template match="preface/section | chapter/section">
  <div class="primary">
    <xsl:apply-templates/>
  </div>
</xsl:template>

<xsl:template match="section/section">
  <div class="secondary">
    <xsl:apply-templates/>
  </div>
</xsl:template>

<!-- Paragraph -->
<xsl:template match="section/section/para">
  <p><xsl:apply-templates/></p>
</xsl:template>

<xsl:template match="preface/section/para[1] | chapter/section/para[1]">
  <p class="para1"><xsl:apply-templates/></p>
</xsl:template>

<xsl:template match="para">
  <p><xsl:apply-templates/></p>
</xsl:template>


<!-- Decorations -->
<xsl:template match="emphasis">
  <em><xsl:apply-templates/></em>  
</xsl:template>

<xsl:template match="quote">
  <q><xsl:apply-templates/></q>
</xsl:template>



    
  



</xsl:stylesheet>
