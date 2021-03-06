# Wireless command documentation

## Command format
- Command structured as series of unsigned chars
  - Prefaced by sender ID
  - Commands can only be sent by controller
  - Command (and args) a single char as defined by an enum (starting with 0x10)
  - Characters below 0x10 are reserved for special use
    -0x00 indicates a reply, 0x01 a status update, 0x0A is reserved for newline applications
  - To drive straight forwards (drive is 0x08), then, would be `01 15 FF FF` (01 is the sender)

- Responses
  - Prefaced by sender ID
  - Can only be sent by nodes
  - Responses encode the original command.
  - 0x00 signals a response, , followed by the original command, and then the payload
  - 0x02 is a response requesting an ACK
  - Response to dump (0x10) would be `FE 00 10 <data>` (FE is the sender)

- ACK
  - Acknowledgement packet
  - sender, 0x03. `01 03` is a confirmation sent by 01

- Updates
  - Prefaced by sender ID
  - 0x01 signals a status update, followed by the update type, then by the packet number, then the expected number of packets
  - A target list update might then be `FE 01 10 00 03 ...`
    - This packet would be the 1st of 4 packets (indexing starts from 0)

## Command list
| Command                  | Type | Mode            | Description                                 |
|--------------------------|------|-----------------|---------------------------------------------|
| dump                     | get  | id or broadcast | Get robot configuration                     |
| set_id <id_num>          | set  | id              | Set robot's ID (0 to 255)                   |
| verbose on/off           | cmd  | id or broadcast | Tell robot to send constant status updates  |
| set_consts <vals>        | set  | id              | Set robot configuration (dump's opposite)   |
| set_const <const> <val>  | set  | id or broadcast | Set specified calibration constant to value |
| stop                     | cmd  | id or broadcast | Shut down motors                            |
| drive <r_spd> <l_spd>    | cmd  | id              | Manually set motor speeds                   |
| set_channel <channel>    | cmd  | id              | Set frequency beacon channel                |
| auto                     | cmd  | id              | Reset manual command overrides              |
