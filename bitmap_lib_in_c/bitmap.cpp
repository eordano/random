#include <string>
#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>

namespace bmps{
    using namespace std;
    struct color{
        int r, g, b;

        color():r(0),g(0),b(0){}
        color(int r, int g, int b):r(r),g(g),b(b){}

        color operator = (const color &c){
            r=c.r; g=c.g; b=c.b;
            return *this;
        }
        const bool operator == (const color &c){
            return r==c.r && g==c.g && b==c.b;
        }

    //End Color
    };

    struct bitmap{
        short magic;
        int size_bmp;
        int unused;
        int offset_data;
        int header_bytes;
        int width;
        int height;
        short color_planes;
        short color_bpp;
        int compression;
        int size_data;
        int h_resolution;
        int v_resolution;
        int colors_palette;
        int mean_palette;
        vector<vector<color> > bmp;
        char *hoax;
        ifstream fin;
        ofstream fout;
        int index;

    //Constructors

        bitmap(){}
        bitmap(const string &file){
            read_bmp(file);
        }
        bitmap(const bitmap &bm){
            *this = bm;
        }
        bitmap(const vector<vector<color> > mapa){
            magic 			= 19778;
            width 			= mapa[0].size();
            height 			= mapa.size();
            size_data 		= height*(width*3+width%4);
            size_bmp 		= 54 + size_data;
            unused 			= 0;
            offset_data 	= 54;
            header_bytes 	= 40;
            color_planes 	= 1;
            color_bpp 		= 24;
            compression 	= 0;
            h_resolution 	= 2835;
            v_resolution 	= 2835;
            colors_palette 	= 0;
            mean_palette 	= 0;
            bmp 			= mapa;
        }

    //Operators

        bool operator = (const bitmap &bm){
            magic 			= bm.magic;
            size_bmp 		= bm.size_bmp;
            unused 			= bm.unused;
            offset_data 	= bm.offset_data;
            header_bytes 	= bm.header_bytes;
            width 			= bm.width;
            height 			= bm.height;
            color_planes 	= bm.color_planes;
            color_bpp 		= bm.color_bpp;
            compression 	= bm.compression;
            size_data 		= bm.size_data;
            h_resolution 	= bm.h_resolution;
            v_resolution 	= bm.v_resolution;
            colors_palette 	= bm.colors_palette;
            mean_palette 	= bm.mean_palette;
            bmp 			= bm.bmp;
            return true;
        }

    //Auxiliary

        template<class T> inline void read_hoax( T& n ){
                n=0;
                for( int i=(sizeof n)-1 ; i>=0 ; i--)
                    n|=hoax[index+i]<<(8*i);
                index+=sizeof n;
        }
        template<class T> inline void write_hoax( const T& n ){
            for( int i=(sizeof n)-1 ; i>=0 ; i-- )
                hoax[index+i]=char(n>>(8*i));
            index+=sizeof n;
        }

    //IO

        void read_bmp(const string &file){
            fin.open(file.c_str(), ios_base::binary);

            //Header
            index = 0;
            hoax = new char[54];
            fin.read(hoax, 54);
            read_hoax( magic );
            read_hoax( size_bmp );
            read_hoax( unused );
            read_hoax( offset_data );
            read_hoax( header_bytes );
            read_hoax( width );
            read_hoax( height );
            read_hoax( color_planes );
            read_hoax( color_bpp );
            read_hoax( compression );
            read_hoax( size_data );
            read_hoax( h_resolution );
            read_hoax( v_resolution );
            read_hoax( colors_palette );
            read_hoax( mean_palette );
            delete hoax;

            //Main
            bmp = vector<vector<color> >(height, vector<color>(width));
            hoax = new char[height*(width*3+width%4)];
            fin.read(hoax, height*(width*3+width%4));
            index = 0;
            for( int i=0; i<height; i++ ){
                for( int j=0; j<width; j++ ){
                    bmp[i][j] = color((unsigned char)hoax[index+2],(unsigned char)hoax[index+1],(unsigned char)hoax[index]);
                    index += 3;
                }
                index += width%4;
            }
            delete hoax;
            fin.close();
        }
        void write_bmp(const string &file){
            fout.open(file.c_str(), ios_base::binary);

            //Header
            hoax = new char[54];
            index = 0;
            write_hoax( magic );
            write_hoax( size_bmp );
            write_hoax( unused );
            write_hoax( offset_data );
            write_hoax( header_bytes );
            write_hoax( width );
            write_hoax( height );
            write_hoax( color_planes );
            write_hoax( color_bpp );
            write_hoax( compression );
            write_hoax( size_data );
            write_hoax( h_resolution );
            write_hoax( v_resolution );
            write_hoax( colors_palette );
            write_hoax( mean_palette );
            fout.write(hoax, 54);
            delete hoax;

            //Main
            hoax = new char[height*(width*3+width%4)];
            index = 0;
            for(int i = 0; i < height; i++){
                for(int j = 0; j < width; j++){
                    hoax[index] = (unsigned char)bmp[i][j].b;
                    hoax[index+1] = (unsigned char)bmp[i][j].g;
                    hoax[index+2] = (unsigned char)bmp[i][j].r;
                    index += 3;
                }
                index += width % 4;
            }
            fout.write(hoax, index);
            fout.close();
            delete hoax;
        }
    };


    double Hue(const color& c){
        int l=c.r,m=c.g,h=c.b;
        if(l>m) swap(l,m);
        if(m>h) swap(m,h);
        if(l>m) swap(l,m);
        double n=(m-l)/(h-l);
        if(c.r>=c.b){
            if(c.g>c.r) return 60*(2-n);
            if(c.g>=c.b) return 60*n;
            return 60*(6-n);
        }
        if(c.g>=c.b) return 60*(2+n);
        if(c.g>c.r) return 60*(4-n);
        return 60*(4+n);
    }

    int Saturation(const color& c){
        int M=max(c.r,max(c.g,c.b)) , m=min(c.r,min(c.g,c.b));
        if(M==m) return 0;
        if((M+m)/2<128)
            return 255*(M-m)/(M+m);
        return 255*(M-m)/(510-M-m);
    }

    int Lightness(const color& c){
        return (299*c.r + 587*c.g + 114*c.b)/2560;
    }
};
