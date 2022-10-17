
// This is the main function which counts the single and coincidence photon detection pulses 
// and sends the corresponding count rates to PC via UART every 1/10th of a second			
module coincidence( output UART_TXD, input clock_50, input A, input B, input C, input D);

// data_trigger is turned on every 1/10th of a second and begins the data stream out
// baud_rate_clk is the clock to output data at the baud rate of 19200 bits/second
    wire baud_rate_clk;
    wire data_trigger;
    wire Coincidence_0;
    wire Coincidence_1; 
    wire Coincidence_2;
    wire Coincidence_3;
    wire Coincidence_4;
    
// Counts the baud clock until it reaches 1920, which occurs every 1/10th of a second
	reg [14:0] data_trigger_count; 
	
// Turns on every 1/10th of a second for one 50 MHz clock pulse signal and resets the photon detection counters
	reg data_trigger_reset; 
	
// Counts the 50 MHz clock pulses until it reaches 2604 in order to time the baud clock	
	reg [31:0] baud_rate_count; 
	
// Represents the top level design entity instantiation of the number of coincidences counted
	wire [31:0] Count_top_0;
	wire [31:0] Count_top_1;
	wire [31:0] Count_top_2;
	wire [31:0] Count_top_3;
	wire [31:0] Count_top_4;

// Output registers of coincident photon counts
	reg [31:0] Count_out_0;
	reg [31:0] Count_out_1;
	reg [31:0] Count_out_2;
	reg [31:0] Count_out_3;
	reg [31:0] Count_out_4;

// Represents the top level design entity instantiation of the number of counts
	wire [31:0] A_top;
	wire [31:0] B_top;
	wire [31:0] C_top;
	wire [31:0] D_top;

// Output registers of single photon counts
	reg [31:0] A_out;
	reg [31:0] B_out;
	reg [31:0] C_out;
	reg [31:0] D_out;

// Generation of four coincidence pulses from the input pulses
	coincidence_pulse CP0( .a(A), .b(B), .y(Coincidence_0));
	coincidence_pulse CP1( .a(A), .b(C), .y(Coincidence_1));
	coincidence_pulse CP3( .a(D), .b(B), .y(Coincidence_2));	
	coincidence_pulse CP2( .a(D), .b(C), .y(Coincidence_3));
//    coincidence_pulse CP4( .a(D), .b(A), .y(Coincidence_4));
	three_detector_coincidence CP4(.a(A), .b(B), .c(C), .y(Coincidence_4));	

// Counts for a baud rate of 19200 and produces the baud rate clock signal 
	baud_rate_counter BRC1 (.clock_50(clock_50), .baud_rate_clk(baud_rate_clk));

// Uses the baud rate clock signal and generates a trigger signal every 1/10th of a second
	data_triggering DT1 (.baud_rate_clk(baud_rate_clk), .data_trigger(data_trigger));

// Outputs the data in 32-bit registers and resets every 1/10th of a second
	counter C0 ( .clock_50(clock_50), .data_trigger(data_trigger), .pulse(Coincidence_0), .q(Count_top_0) );
	counter C1 ( .clock_50(clock_50), .data_trigger(data_trigger), .pulse(Coincidence_1), .q(Count_top_1) );
	counter C2 ( .clock_50(clock_50), .data_trigger(data_trigger), .pulse(Coincidence_2), .q(Count_top_2) );
	counter C3 ( .clock_50(clock_50), .data_trigger(data_trigger), .pulse(Coincidence_3), .q(Count_top_3) );
    counter C4 ( .clock_50(clock_50), .data_trigger(data_trigger), .pulse(Coincidence_4), .q(Count_top_4) );
    counter CA ( .clock_50(clock_50), .data_trigger(data_trigger), .pulse(A), .q(A_top));
	counter CB ( .clock_50(clock_50), .data_trigger(data_trigger), .pulse(B), .q(B_top));
	counter CC ( .clock_50(clock_50), .data_trigger(data_trigger), .pulse(C), .q(C_top));
	counter CD ( .clock_50(clock_50), .data_trigger(data_trigger), .pulse(D), .q(D_top));

	
// This process updates the counts output arrays every 1/10th of a second
	always@( posedge data_trigger)
		begin
		A_out <= A_top;
		B_out <= B_top;
		C_out <= C_top;
		D_out <= D_top;
		Count_out_0 <= Count_top_0;
		Count_out_1 <= Count_top_1;
		Count_out_2 <= Count_top_2;
		Count_out_3 <= Count_top_3;
		Count_out_4 <= Count_top_4;
		end
	
// Sends the A, B, C, D and the Coincidence counts out on the RS-232 port
	data_out D0 ( .A(A_out), .B(B_out), .C(C_out), .D(D_out), .coincidence_0(Count_out_0), 
	.coincidence_1(Count_out_1), .coincidence_2(Count_out_2), .coincidence_3(Count_out_3), .coincidence_4(Count_out_4), 
	.clk(baud_rate_clk), .data_trigger(data_trigger), .UART_TXD(UART_TXD));

endmodule


// This function ANDs two pulse signals to form one coincidence pulse signal
module coincidence_pulse (input a, input b, output reg y);

	always @(*)
		begin
		y = a && b;
		end

endmodule

module three_detector_coincidence (input a, input b, input c, output reg y);
    
    always @(*)
        begin
        y = a && b && c;
        end
        
endmodule


// This function uses the baud rate clock signal and generates a trigger signal 
// every 1/10th of a second
module data_triggering (input baud_rate_clk, output reg data_trigger);

reg [31:0] data_trigger_count;

	always @(posedge baud_rate_clk)
	
		begin
		data_trigger_count <= data_trigger_count  +1;
		if (data_trigger_count == 12'b11110000000)//15'b100101100000000) //Currently set to 1,920 so we get clock of 10Hz
			begin
			data_trigger <= 1;
			data_trigger_count <=0;
			end
		else
			data_trigger <= 0;	
	   end

endmodule	

// This counter specifically counts for a baud rate of 19200 and produces a 
// corresponding baud rate clock signal 
module baud_rate_counter (input clock_50, output reg baud_rate_clk);

reg [31:0] baud_rate_count;

	always@(posedge clock_50)
		begin
		baud_rate_count <= baud_rate_count +1;

		if (baud_rate_count >= 5208)
		begin
			baud_rate_clk <= 1;
			baud_rate_count <=0;
		end

		else
			baud_rate_clk <= 0;		
	   end

endmodule

// This function counts voltage pulses
module counter(input clock_50, input data_trigger, input pulse, output reg [31:0]q);

	wire x;

	or o1 (x, data_trigger, pulse);

	always @ (posedge x)
		begin

		if (data_trigger)
			q <=0;

		else
			q<=q+1;

		end
		
endmodule

// This function sends out up to four single photon counts and up to four coincidence counts
// to the PC through serial communication (UART)
module data_out(input [31:0] A, input [31:0] B, input [31:0] C, input [31:0] D, 
input [31:0] coincidence_0, input [31:0] coincidence_1, input [31:0] coincidence_2, 
 input [31:0] coincidence_3, input [31:0] coincidence_4, input clk, input data_trigger, output reg UART_TXD);

	reg [5:0] index;
	reg [0:31] incremental;
	reg [31:0] out;
	reg [3:0] data_select;

	always @ (posedge clk)

		begin
		
		if (index == 6'b111111 && data_trigger == 1)
			begin
			index <= 6'b000000;
			UART_TXD <= 1;
			//out <= 32'b11111110101010111111101010101111;
			out <= 32'b10011001100010010101010101011101;
			              
			data_select <= 3'b000;
			end
		
		else if (index == 6'b000000)
			begin
			index <= 6'b000001;
			UART_TXD <= 0;
			end
		
		else if (index == 6'b000001)
			begin
			index <= 6'b000010;
			UART_TXD <= out[0];
			end	
		
		else if (index == 6'b000010)
		   begin
			index <= 6'b000011;
			UART_TXD <= out[1];
			end
			
		else if (index == 6'b000011)
			begin
			index <= 6'b000100;
			UART_TXD <= out[2];
			end
			
		else if (index == 6'b000100)
			begin
			index <= 6'b000101;
			UART_TXD <= out[3];
			end
			
		else if (index == 6'b000101)
			begin
			index <= 6'b000110;
			UART_TXD <= out[4];
			end
			
		else if (index == 6'b000110)
			begin
			index <= 6'b000111;
			UART_TXD <= out[5];
			end	
	
		else if (index == 6'b000111)
			begin
			index <= 6'b001000;
			UART_TXD <= out[6];
			end
			
		else if (index == 6'b001000)
			begin
			index <= 6'b001001;
			UART_TXD <= 0; 
			end
			
		else if (index == 6'b001001)
			begin
			index <= 6'b001010;
			UART_TXD <= 1; // the first stop bit
			end
			
		else if (index == 6'b001010)
			begin
			index <= 6'b001011;
			UART_TXD <= 0; // the second start bit
			end
			
		else if (index == 6'b001011)
			begin
			index <= 6'b001100;
			UART_TXD <= out[7];
			end
			
		else if (index == 6'b001100)
			begin
			index <= 6'b001101;
			UART_TXD <= out[8];
			end
			
		else if (index == 6'b001101)
			begin
			index <= 6'b001110;
			UART_TXD <= out[9];
			end
			
		else if (index == 6'b001110)
			begin
			index <= 6'b001111;
			UART_TXD <= out[10];
			end
			
		else if (index == 6'b001111)
			begin
			index <= 6'b010000;
			UART_TXD <= out[11];
			end
			
		else if (index == 6'b010000)
			begin
			index <= 6'b010001;
			UART_TXD <= out[12];
			end
			
		else if (index == 6'b010001)
			begin
			index <= 6'b010010;
			UART_TXD <= out[13];
			end
			
		else if (index == 6'b010010)
			begin
			index <= 6'b010011;
			UART_TXD <= 0; // the termination bit
			end
			
		else if (index == 6'b010011)
			begin
			index <= 6'b010100;
			UART_TXD <= 1; // the second stop bit
			end
			
		else if (index == 6'b010100)
			begin
			index <= 6'b010101;
			UART_TXD <= 0; // the third start bit
			end
			
		else if (index == 6'b010101)
			begin
			index <= 6'b010110;
			UART_TXD <= out[14];
			end
			
		else if (index == 6'b010110)
			begin
			index <= 6'b010111;
			UART_TXD <= out[15];
			end
			
		else if (index == 6'b010111)
			begin
			index <= 6'b011000;
			UART_TXD <= out[16];
			end
			
		else if (index == 6'b011000)
			begin
			index <= 6'b011001;
			UART_TXD <= out[17];
			end
			
		else if (index == 6'b011001)
			begin
			index <= 6'b011010;
			UART_TXD <= out[18];
			end	
			
		else if (index == 6'b011010)
			begin
			index <= 6'b011011;
			UART_TXD <= out[19];
			end
			
		else if (index == 6'b011011)
			begin
			index <= 6'b011100;
			UART_TXD <= out[20];
			end
			
		else if (index == 6'b011100)
			begin
			index <= 6'b011101;
			UART_TXD <= 0; // the termination bit
			end
			
		else if (index == 6'b011101)
			begin
			index <= 6'b011110;
			UART_TXD <= 1; // the third stop bit
			end
			
		else if (index == 6'b011110)
			begin
			index <= 6'b011111;
			UART_TXD <= 0; // the fourth start bit
			end
			
		else if (index == 6'b011111)
			begin
			index <= 6'b100000;
			UART_TXD <= out[21];
			end
			
		else if (index == 6'b100000)
			begin
			index <= 6'b100001;
			UART_TXD <= out[22];
			end
			
		else if (index == 6'b100001)
			begin
			index <= 6'b100010;
			UART_TXD <= out[23];
			end
			
		else if (index == 6'b100010)
			begin
			index <= 6'b100011;
			UART_TXD <= out[24];
			end	
			
		else if (index == 6'b100011)
			begin
			index <= 6'b100100;
			UART_TXD <= out[25];
			end	
			
		else if (index == 6'b100100)
			begin
			index <= 6'b100101;
			UART_TXD <= out[26];
			end	
			
		else if (index == 6'b100101)
			begin
			index <= 6'b100110;
			UART_TXD <= out[27];
			end	
			
		else if (index == 6'b100110)
			begin
			index <= 6'b100111;
			UART_TXD <= 0;  // termination bit			
			end	
				
		else if (index == 6'b100111)
			begin
			index <= 6'b101000;
			UART_TXD <= 1; // the fourth stop bit
			end	
			
		else if (index == 6'b101000)
			begin
			index <= 6'b101001;
			UART_TXD <= 0; // the fifth start bit
			end
			
		else if (index == 6'b101001)
			begin
			index <= 6'b101010;
			UART_TXD <= out[28];
			end
			
		else if (index == 6'b101010)
			begin
			index <= 6'b101011;
			UART_TXD <= out[29];
			end	
			
		else if (index == 6'b101011)
			begin
			index <= 6'b101100;
			UART_TXD <= out[30];
			end	
			
		else if (index == 6'b101100)
			begin
			index <= 6'b101101;
			UART_TXD <= out[31];
			end	
			
		else if (index == 6'b101101)
			begin
			index <= 6'b101110;
			UART_TXD <= 0;
			end
			
		else if (index == 6'b101110)
			begin
			index <= 6'b101111;
			UART_TXD <= 0;
			end
			
		else if (index == 6'b101111)
			begin
			index <= 6'b110000;
			UART_TXD <= 0;
			end	
			
		else if (index == 6'b110000)
			begin
			index <= 6'b110001;
			UART_TXD <= 0;			
			end	
			
		else if (index == 6'b110001 && data_select == 4'b0000)
            begin
            index <= 6'b000000;
            data_select <= 4'b0001; // increments data_select to begin output of B
            out <= A;
            //out <= 32'b1;
            //incremental <= incremental + 100;
            //out <= incremental;
            UART_TXD <= 1; // the fifth stop bit            
            end    
		
		else if (index == 6'b110001 && data_select == 4'b0001)
			begin
			index <= 6'b000000;
			data_select <= 4'b0010; // increments data_select to begin output of B
			out <= B;
			//out <= 32'b10000100011101000110101110001110;
			//out <= 32'b10;
			UART_TXD <= 1; // the fifth stop bit			
			end	

		else if (index == 6'b110001 && data_select == 4'b0010)
			begin
			index <= 6'b000000;
			data_select <= 4'b0011; // increments data_select to begin output of C
			out <= C;
            //out <= 32'b11000110101011101010000101010101;
            //out <= 32'b11;
			UART_TXD <= 1; // the fifth stop bit
			end	
				
		else if (index == 6'b110001 && data_select == 4'b0011)
			begin
			index <= 6'b000000;
			data_select <= 4'b0100; // increments data_select to begin output of D
			out <= D;
            //out <= 32'b00011010011111011010111100011100;
			//out <= 32'b100;
			UART_TXD <= 1; // the fifth stop bit
			end
			
		else if (index == 6'b110001 && data_select == 4'b0100)
			begin
			index <= 6'b000000;
			data_select <= 4'b0101; // increments data_select to begin output of Coincidence_0
			out <= coincidence_0;
			//out <= 32'b00100001000111010001101011100011;
			//out <= 32'b101;
			UART_TXD <= 1; // the fifth stop bit
			end	
				
		else if (index == 6'b110001 && data_select == 4'b0101)
			begin
			index <= 6'b000000;
			data_select <= 4'b0110; // increments data_select to begin output of Coincidence_1
			out <= coincidence_1;
			//out <= 32'b00100111101111001000011010101010;
			//out <= 32'b110;
			UART_TXD <= 1; // the fifth stop bit
			end	
				
		else if (index == 6'b110001 && data_select == 4'b0110)
			begin
			index <= 6'b000000;
			data_select <= 4'b0111; // increments data_select to begin output of Coincidence_2
			out <= coincidence_2;
			//out <= 32'b0100101000101100101101110001;
			//out <= 32'b111;
			UART_TXD <= 1; // the fifth stop bit
			end	
				
		else if (index == 6'b110001 && data_select == 4'b0111)
			begin
			index <= 6'b000000;
			data_select <= 4'b1000; // increments data_select to begin output of Coincidence_3
			out <= coincidence_3;
		    //out <= 32'b0101010011000101011000111000;
		    //out <= 32'b1000;
			UART_TXD <= 1; // the fifth stop bit
			end	
			
		else if (index == 6'b110001 && data_select == 4'b1000)
            begin
            index <= 6'b000000;
            data_select <= 4'b1001; // increments data_select to begin output of Coincidence_4
            out <= coincidence_4;
            UART_TXD <= 1; // the fifth stop bit
            end    
				
		else if (index == 6'b110001 && data_select == 4'b1001)
			begin
			index <= 6'b110010;
			UART_TXD <= 1; // the fifth stop bit
			end	
				
		else if (index == 6'b110010)
			begin
			index <= 6'b111111;
			UART_TXD <= 0; // the start bit of the termination byte
			end
			
		else 
			begin
			index <= 6'b111111;
			UART_TXD <= 1; // sets all subsequent bits to negative voltage
			end
	end

endmodule