<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <!-- Identity template to copy everything by default -->
    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>

    <!-- Template to match RecycleData elements and keep their path -->
    <xsl:template match="RecycleData">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>

    <!-- Template to remove all elements except those containing RecycleData -->
    <xsl:template match="*[not(descendant-or-self::RecycleData)]">
        <xsl:apply-templates select="RecycleData"/>
    </xsl:template>

    <!-- Template to remove whitespace-only text nodes -->
    <xsl:template match="text()[normalize-space()='']"/>
</xsl:stylesheet>

