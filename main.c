#include <gb/gb.h>

#include "tiles.c"
#include "map.c"

void main()
{
     set_bkg_data(0, 255, TileData);
     set_bkg_tiles(0, 0, 20, 18, MapData);
     SHOW_BKG;
     DISPLAY_ON; 
}
