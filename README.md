## Project Demonstration

To find a brief minute demonstration of this project in early stages of development, go here:  
[Watch Demonstration](https://drive.google.com/file/d/1QJ15o_uG3ZQs_LL5cbMobzL5gI6KKKRl/view?usp=drive_link)

## Running Configurations

### Instructions to Run

1. Open CMD by clicking on the bottom left of your screen and typing "CMD".
2. Use the following command format to run the executable:

    ```bash
    filename.exe -a -b -c -d -e -f -g
    ```

### Parameters

- **`-a`**: Lower color range (HSV), entered as `1,2,3` or `120,320,3333`.  
  _(Numbers are just examples; you may enter your own values, but the format must remain the same.)_  
  **Optional** (###)

- **`-b`**: Upper color range (HSV), entered as `1,2,3` or `120,320,3333`.  
  _(Numbers are just examples; you may enter your own values, but the format must remain the same.)_  
  **Optional** (###)

- **`-c`**: Camera source number. By default, it is set to `1`. If this doesn't work, try `0`.  
  **Optional** (###)

- **`-d`**: **IP Address of the Arduino webserver.**  
  **Required** (***).  
  Format like: `x.x.x.x` (Example: `192.168.1.1`).

- **`-e`**: Minimum area for an object to be identified. Default is `200`.  
  May require tweaking depending on the camera's Field of View (FOV).  
  **Optional** (###)

- **`-f`**: Time in between checking the object count. Default is every `60` seconds.  
  **Optional** (###)

- **`-g`**: Number of objects that is considered too many. Default is `10` every `60` seconds.  
  **Optional** (###)

### Example Runs

- `Main.exe -c 0 -d IP_ADDRESS`

- `Main.exe -a 0,51,0 -b 12,255,255 -c 0 -d 192.168.20.2 -e 1000 -f 20 -g 5`

- `Main.exe -c 0 -d IP_ADDRESS -e 150 -f 12 -g 8`

**Note**: Press `B` to exit the application.
