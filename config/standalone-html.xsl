<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0"
		xmlns:xsl="http://www.w3.org/1999/XSL/Transform" >


  <xsl:template match="/">
    <html>
      <head>
      </head>
      <body>
	<xsl:apply-templates/>
      </body>
    </html>
  </xsl:template>


  <xsl:template match="preface | chapter">
    <div class="primary">
      <xsl:apply-templates/>
    </div>
  </xsl:template>


  <xsl:template match="chapter/section | preface/section">
    <div class="secondary">
      <xsl:apply-templates/>
    </div>
  </xsl:template>

  <xsl:template match="section/section/section">
    <div class="quadrinary">
      <xsl:apply-templates/>
    </div>
  </xsl:template>

  <xsl:template match="section/section">
    <div class="tertiary">
      <xsl:apply-templates/>
    </div>
  </xsl:template>

  <xsl:template match="title">
    <title><xsl:apply-templates/></title>
  </xsl:template>

  <xsl:template match="para">
    <p><xsl:apply-templates/></p>
  </xsl:template>

  <xsl:template match="emphasis">
    <emphasis><xsl:apply-templates/></emphasis>
  </xsl:template>

  <xsl:template match="quote">
    "<xsl:apply-templates/>
  </xsl:template>

</xsl:stylesheet>
