#include <math.h>

#include "xtrack_tracker.h"
#include "sim_config.h"

#include <stdio.h>
#include <stdlib.h>

int8_t* file_to_buffer(char *filename, int8_t* buf_in){

    FILE *sim_fid;
    int8_t *buf;

    // Get buffer
    sim_fid = fopen(filename, "rb");
    if (!sim_fid){
        return NULL;
    }
    fseek(sim_fid, 0L, SEEK_END);
    unsigned long filesize = ftell(sim_fid);
    fseek(sim_fid, 0L, SEEK_SET);
    if (buf_in){
        printf("Reusing buffer\n");
        buf = buf_in;
    }
    else{
        buf = malloc(filesize*sizeof(int8_t));
    }
    fread(buf, sizeof(int8_t), filesize, sim_fid);
    fclose(sim_fid);

    return (buf);
}

int main(){


    int8_t* sim_buffer = file_to_buffer("./xboinc_input.bin", NULL);
    if (!sim_buffer){
        printf("Error: could not read simulation input file\n");
        return -1;
    }

    // Get sim config
    SimConfig sim_config = (SimConfig) sim_buffer;

    const int64_t num_turns = SimConfig_get_num_turns(sim_config);
    const int64_t num_elements = SimConfig_get_num_elements(sim_config);

    //printf("num_turns: %d\n", (int) num_turns);
    //printf("num_elements: %d\n", (int) num_elements);

    ParticlesData particles = SimConfig_getp_sim_state_particles(sim_config);
    SimStateData sim_state = SimConfig_getp_sim_state(sim_config);
    int64_t checkpoint_every = SimConfig_get_checkpoint_every(sim_config);

    // Check if checkpoint exists
    printf("sim_state: %p\n", (int8_t*) sim_state);
    int8_t* loaded = file_to_buffer("./checkpoint.bin", (int8_t*) sim_state);
    //if (loaded){
    //    printf("Loaded checkpoint\n");
    //}
    //else{
    //    printf("No checkpoint found\n");
    //}

    while (SimStateData_get_i_turn(sim_state) < num_turns){
        track_line(
            sim_buffer, //    int8_t* buffer,
            SimConfig_getp_line_metadata(sim_config), //ElementRefData elem_ref_data
            particles, //    ParticlesData particles,
            1, //    int num_turns,
            0, //    int ele_start,
            (int) num_elements, //    int num_ele_track,
            1, //int flag_end_turn_actions,
            1, //int flag_reset_s_at_end_turn,
            0, //    int flag_monitor,
            0, //   int64_t num_ele_line, (needed only for backtracking)
            0.0, //    double line_length, (needed only for backtracking)
            NULL,//    int8_t* buffer_tbt_monitor,
            0, //    int64_t offset_tbt_monitor
            NULL//    int8_t* io_buffer,
        );
        SimStateData_set_i_turn(sim_state, SimStateData_get_i_turn(sim_state) + 1);

        if (checkpoint_every>0){
            if (SimStateData_get_i_turn(sim_state) % checkpoint_every == 0){
                //printf("Checkpointing turn %d!\n", (int) SimStateData_get_i_turn(sim_state));
                FILE *chkp_fid;
                chkp_fid = fopen("./checkpoint.bin", "wb");
                fwrite(SimConfig_getp_sim_state(sim_config), sizeof(int8_t),
                    SimConfig_get_sim_state_size(sim_config), chkp_fid);
                fclose(chkp_fid);
            }
        }
    }

    // Quick check
    //for (int ii=0; ii<ParticlesData_get__capacity(particles); ii++){
        //printf("s[%d] = %e\n", ii, ParticlesData_get_s(particles, (int64_t) ii));
    //}

    // Save output
    FILE *out_fid;
    out_fid = fopen("./sim_state_out.bin", "wb");
    fwrite(SimConfig_getp_sim_state(sim_config), sizeof(int8_t),
           SimConfig_get_sim_state_size(sim_config), out_fid);
    fclose(out_fid);

    // Remove checkpoint
    if (remove("./checkpoint.bin") != 0){
        printf("Error: could not remove checkpoint file\n");
        return -1;  // error
    }
    else{
        //printf("Checkpoint file removed\n");
    }

    return 0;
}
