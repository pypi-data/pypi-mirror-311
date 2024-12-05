/*
 * Copyright (c) 1991 Stanford University
 * Copyright (c) 1991 Silicon Graphics, Inc.
 *
 * Permission to use, copy, modify, distribute, and sell this software and 
 * its documentation for any purpose is hereby granted without fee, provided
 * that (i) the above copyright notices and this permission notice appear in
 * all copies of the software and related documentation, and (ii) the names of
 * Stanford and Silicon Graphics may not be used in any advertising or
 * publicity relating to the software without the specific, prior written
 * permission of Stanford and Silicon Graphics.
 * 
 * THE SOFTWARE IS PROVIDED "AS-IS" AND WITHOUT WARRANTY OF ANY KIND, 
 * EXPRESS, IMPLIED OR OTHERWISE, INCLUDING WITHOUT LIMITATION, ANY 
 * WARRANTY OF MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE.  
 *
 * IN NO EVENT SHALL STANFORD OR SILICON GRAPHICS BE LIABLE FOR
 * ANY SPECIAL, INCIDENTAL, INDIRECT OR CONSEQUENTIAL DAMAGES OF ANY KIND,
 * OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
 * WHETHER OR NOT ADVISED OF THE POSSIBILITY OF DAMAGE, AND ON ANY THEORY OF 
 * LIABILITY, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE 
 * OF THIS SOFTWARE.
 */

/*
 * PolyGlyph -- list of glyphs
 */

#ifndef iv_polyglyph_h
#define iv_polyglyph_h

#include <InterViews/glyph.h>

#include <InterViews/_enter.h>

class PolyGlyphImpl;

class PolyGlyph : public Glyph {
public:
    PolyGlyph(GlyphIndex initial_size = 10);
    virtual ~PolyGlyph();

    virtual void undraw();

    virtual void append(Glyph*);
    virtual void prepend(Glyph*);
    virtual void insert(GlyphIndex, Glyph*);
    virtual void remove(GlyphIndex);
    virtual void replace(GlyphIndex, Glyph*);
    virtual void change(GlyphIndex);

    virtual GlyphIndex count() const;
    virtual Glyph* component(GlyphIndex) const;

    virtual void modified(GlyphIndex);
private:
    PolyGlyphImpl* impl_;
};

#include <InterViews/_leave.h>

#endif
