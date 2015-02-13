<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0"
		xmlns:xsl="http://www.w3.org/1999/XSL/Transform">


  <xsl:template match="/">
    \documentclass{article}

    \begin{document}
       <xsl:apply-templates/>
    \end{document}
    
  </xsl:template>


  <xsl:template match='chapter/section | preface/section'>
    \section{<xsl:value-of select="title"/>}
    <xsl:apply-templates/>
  </xsl:template>

  <xsl:template match='section/section/section'>
    \subsubsection{<xsl:value-of select="title"/>}
    <xsl:apply-templates/>
  </xsl:template>

  <xsl:template match="section/section">
    \subsection{<xsl:value-of select="title"/>}
    <xsl:apply-templates/>
  </xsl:template>

  <xsl:template match="para">

    <xsl:apply-templates/>
    
  </xsl:template>

  <xsl:template match="emphasis">
    \emph{<xsl:apply-templates/>}
  </xsl:template>

  <xsl:template match="quote">
    ``<xsl:apply-templates/>''
  </xsl:template>

  
  <xsl:template match='section/title'/>






  

</xsl:stylesheet>
