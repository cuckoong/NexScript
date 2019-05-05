#include <SoftwareSerial.h>
#include <DFPlayer_Mini_Mp3.h>

SoftwareSerial mySerial(10, 11); // RX, TXen


const int Llight = 7; // left light, PH4
const int Rlight = 8; // right light, PH5
const int BUSY = 12; //
const int MLLight = 20; // left masking light, PD1
const int MRLight = 21; // Right masking light, PD0
const int LRED = 18; //left infrad red led, PD3
const int RRED = 19; //right infrad red led, PD2
const int Ls = 49; //PORTL0
const int Ms = 48; //PORTL1
const int Rs = 47; //PORTL2
const int Lwater = 5; //PE3
const int Rwater = 3; //PE5
int RewardTime_Left = 100;
int RewardTime_Right = 100;
const int sendTime = 200;
const unsigned long CUEhold = 1000;
const unsigned long LightHold = 1000;
const int inTime = 3000;
const unsigned long TrialWait = 3000;
const int LightWaitTime = 140;


String readString;
char a = 'b';

int val = 0;  //0,for no poke, 1 for poke the left, 2 middle, 3 right
int mode = -1;
boolean Ll = false;
boolean Rl = false;
long StS;
unsigned long LightTime;
unsigned long CueTime;
unsigned long TrialStart;
unsigned long StiTime;
boolean Up = false;
boolean Dn = false;
boolean HL = false;
//1 brown noise 2 blue noise 3 HF 4 LF
int Mark[11] = {33, 23, 24, 25, 26, 27, 28, 29, 30, 34, 35};
int BusyPin = 33; //the 12th line
//M0 L_PORT M1 M_PORT M2 R_PORT M3 L_WATER M4 R_WATER M5 MUSIC_1 M6 MUSIC_2 M7 MUSIC_3 M8 MUSIC_4
//M9 L_LIGHT M10 R_LIGHT
//no code for the 16th pin, it share with the mp3 busy pin
boolean MarkHL = true; //LOW for signal
int intt = 300;
int CurrentState = 0;
int PreviousState;

//The OmniPlex D System differentiates strobes coming from Ports A and B 
//by adding a sixteenth bit to the strobes coming from Port B. 
//This adds the number 32768 to strobes coming from Port B, 
//and the software considers any number over 32768 as originating from Port B.
//connect port A in plexon
const int GOutPut = B00000001;
const int AOutPut = B11111110; 
//const int RedOutPut = B00000000;
// for the time stamp input pin here, 
//PORTC include{30,31,32,33,34,35,36,37}
//PORTG include {x,x,4,x,x,39,40,41(strobe)}
//PORTA include{29,28,27,26,25,24,23,22}
//PORTE include{X,X,3,2,5,X,1,0}


// L_WATER B01000000   V ---64
// M_PORT  B00000010 (TrialStart)V ---2
// M_PORT  B00010000 (exit)V ----16  
// L_PORT  B00011010  V---26
// R_PORT  B00000100  V ---4
// BrownNo B00000110  V ---6
// BlueNoi B00001100  V --- 12
// R_WATER B00001010  V---10
// s- LR B00010100   V ---20  //small left reward
// s- RR B00110100   V --- 52 //small right reward
// wrongTr B00110000  V --- 48
// earlyTe B01110000  V ---112
// omissio B11110000  V ---240
//TrialEnd B11110010  V ---242


// Brown/Ll       B01010100 --84
// Brown/Rl       B01000100 --68
// Blue /Ll       B01111100 --124
// Blue /Rl       B01000110 --70


void setup() {
  Serial.begin(115200);
  mySerial.begin (9600);
  mp3_set_serial (mySerial);  //set softwareSerial for DFPlayer-mini mp3 module
  delay(500);  //wait 1ms for mp3 module to set volume
  mp3_set_volume (30);  //0-30
  delay(sendTime);

  
  //set as output

  //  time stamp
DDRG = DDRG | B00000001;
DDRA = DDRA | B11111111;

//water control, 
  DDRE = DDRE | B00101000;

//left/right light
  DDRH = DDRH | B00110000;

//masking light AND infra-red light
  DDRD = DDRD | B00001111;



pinMode(13, OUTPUT);
digitalWrite(13, LOW);
  

//Default setting for water control
PORTE = B00000000;

//default setting for left/right light
PORTH = B00000000;

//default setting for masking light AND red light
PORTD = B00001111;


  Serial.println('a');
  a = 'b';
  while (a != 'a') {
    a = Serial.read();
  }

}

void loop() {

  if (Serial.available() > 0) {
    mode = Serial.read();
    val = 0;
    switch (mode) {
      case 'T': //check central port
      val = ~PINL & B00000111;
      Serial.println(val,DEC);  
        CurrentState = val; 
         //number 1- left; number 2- middle; number  4- right

//send the time stamp signal only when the port state change and the current state is the central poke
        if((CurrentState != PreviousState) && (CurrentState == 2))
        {
            PORTA = B00000010;
            PORTG = B00000000;
            PORTG = B00000001;
            delay(1);
            PORTG = B00000000;
            PreviousState = CurrentState; //update the current state
          //time stamp for the infra-red sensor
        }else{
          PreviousState = CurrentState; //update the current state
        }
        break;

        case 't':  //check side port
       val = ~PINL & B00000111; 
       Serial.println(val,DEC);  
        CurrentState = val; 
         //number 1- left; number 2- middle; number  4- right
       //send the time stamp signal only when the port state change and the current state is the side poke
        if((CurrentState != PreviousState) && (CurrentState == 1))
        {
            PORTA = B00011010;
            PORTG = B00000000;
            PORTG = B00000001;
            delay(1);
            PORTG = B00000000;
            PreviousState = CurrentState; //update the current state
          //time stamp for the infra-red sensor
        }
        else if((CurrentState != PreviousState) && (CurrentState == 4))
        {
          PORTA = B00000100;
          PORTG = B00000000;
          PORTG = B00000001;
          delay(1);
          PORTG = B00000000;
          PreviousState = CurrentState; //update the current state
          //time stamp for the infra-red sensor
        }
        else
        {
          PreviousState = CurrentState; //update the current state
        }
        break;


         case 'H':  //check central port exit
      val = ~PINL & B00000111;
        CurrentState = val; 
         Serial.println(val,DEC);   
         //number 1- left; number 2- middle; number  4- right
        //send the time stamp signal only when the port state change and the current state is the central exit
        if((CurrentState != PreviousState) && (CurrentState ==  0))
        {
            PORTA = B00010000;  //exit from the central port;
            PORTG = B00000000;
            PORTG = B00000001;
            delay(1);
            PORTG = B00000000;
            PreviousState = CurrentState;
          //time stamp for the infra-red sensor
        }else{
          PreviousState = CurrentState;
        }
        break;


      case 'F':
      // off the masking light
      PORTD = B00001100;
      break;

      case 'N':
      // on the masking light
      PORTD = B00001111;
      break;

      case 'L':
        mp3_play(20);
        PORTE = B00001000; //left water valve 
        PORTA = B01000000;  //left water valve time stamp
        PORTG = B00000000;  //strobe
        PORTG = B00000001;  //strobe
        delay(1);
        PORTG = B00000000;  //strobe 
        RewardTime_Left = 80;
        delay(RewardTime_Left);
        PORTE = B00000000;
        PORTA = B11110010; //trial end
        PORTG = B00000001;
        delay(1);
        PORTG = B00000000; 
        break;

      case 'R':
        mp3_play(20);
        PORTE = B00100000; //right water valve 
        PORTA = B00001010;  //right water valve time stamp   
        PORTG = B00000000;  //strobe   
        PORTG = B00000001;  //strobe
        delay(1);
        PORTG = B00000000;  //strobe
        RewardTime_Right = 60;
        delay(RewardTime_Right);
        PORTE = B00000000;
        PORTA = B11110010; //trial end
        PORTG = B00000001;
        delay(1);
        PORTG = B00000000; 
        break;

      case 'A':
      //left side
        mp3_play(20);
        PORTE = B00001000; //left water valve 
        delay(RewardTime_Left);
        PORTE = B00000000;
        break;

      case 'B':
      //right side
        mp3_play(20);
        PORTE = B00100000; //right water valve 
        delay(RewardTime_Right);
        PORTE = B00000000;
        break;

      case 'C':
        digitalWrite(Lwater, HL);
        digitalWrite(Rwater, HL);
        break;


      case 'E':    //CUE(Brown noise)
        //cue begin
          mp3_play(1); 
          StS = millis();
        while (millis() - StS < sendTime) {
           if (!digitalRead(BUSY))break;
        }
        PORTA = B00000110;
        PORTG = B00000000;  //strobe
        PORTG = B00000001;
        delay(1);
        PORTG = B00000000;
        break;

      case 'U':     //CUE (blue noise)
        //cue begin
          mp3_play(2);
          StS = millis();
          while (millis() - StS < sendTime) {
            if (!digitalRead(BUSY))break;
          }
        PORTA = B00001100;
        PORTG = B00000000; 
        PORTG = B00000001;
        delay(1);
        PORTG = B00000000;      
        break;

        case 'f':    // Brown/ LEFT LIGHT until response
        Ll = true;
        LightTime = millis();
        PORTA = B01010100;
        PORTG = B00000000; 
        PORTG = B00000001;
        delay(1);
        PORTG = B00000000; 
        break;

        case 'o':     //Brown/ RIGHT LIGHT
        //StS = millis();
        //  while (millis() - StS < LightWaitTime) {
            //wait for light - sound delay
        //  }
        Rl = true;//light on
        LightTime = millis();
        PORTA = B01000100;
        PORTG = B00000000; 
        PORTG = B00000001;
        delay(1);
        PORTG = B00000000; 
        break;

      case 'v':     //Blue/ LEFT LIGHT until response
        Ll = true;
        LightTime = millis();
        PORTA = B01111100;
        PORTG = B00000000; 
        PORTG = B00000001;
        delay(1);
        PORTG = B00000000;       
        break;

      case 'w':     //Blue/ RIGHT LIGHT
        Rl = true;//light on
        LightTime = millis();
        PORTA = B01000110;
        PORTG = B00000000; 
        PORTG = B00000001;
        delay(1);
        PORTG = B00000000; 
        break;



        case 'M': //Wrong trials
        mp3_stop();
        Ll = false;
        Rl = false;
        PORTH = B00000000; //Off the left/right light
        PORTD = B00001100; // off the masking light

        PORTA = B00110000; //wrong trials
        PORTG = B00000000; 
        PORTG = B00000001;
        delay(1);
        PORTG = B00000000; 
        PORTA = B11110010; //trial end
        PORTG = B00000001;
        delay(1);
        PORTG = B00000000; 
        break;

        case 'h': //omission
        mp3_stop();
        Ll = false;
        Rl = false;
        PORTH = B00000000; //Off the left/right light

        PORTA = B11110000; //omission
        PORTG = B00000000; 
        PORTG = B00000001;
        delay(1);
        PORTG = B00000000;
        PORTA = B11110010; //trial end
        PORTG = B00000001;
        delay(1);
        PORTG = B00000000;        
        break;


      case 'X':
        mp3_stop();
        Ll = false;
        Rl = false;
        PORTH = B00000000; //Off the left/right light
        break;

      case 'x': //early termination
        mp3_stop();
        Ll = false;
        Rl = false;
        PORTH = B00000000; //Off the left/right light

        PORTA = B01110000; //early termination
        PORTG = B00000000; 
        PORTG = B00000001;
        delay(1);
        PORTG = B00000000; 
        PORTA = B11110010; //trial end
        PORTG = B00000001;
        delay(1);
        PORTG = B00000000; 
        break;
        

      case 'S':
        readString = "";
        a = 'b';
        while (a != '#') {
          a = Serial.read();
          if (a == '#') {
            break;
          } else if (a != -1) {
            readString += a;
          }
        }
        RewardTime_Left = readString.toInt();
        digitalWrite(13, HIGH);
        digitalWrite(13, LOW);
        break;

      case 'D':
        readString = "";
        a = 'b';
        while (a != '#') {
          a = Serial.read();
          if (a == '#') {
            break;
          } else if (a != -1) {
            readString += a;
          }
        }
        RewardTime_Right = readString.toInt();
        digitalWrite(13, HIGH);
        digitalWrite(13, LOW);
        break;
    }
  }

  if (Ll & (millis() - LightTime) % 500 < 300) { //left light continue to flash
    //digitalWrite(Llight, HL);
    PORTH = B00010000;
  } else if (Ll & (millis() - LightTime) % 500 > 300) {
    //digitalWrite(Llight, !HL);
    PORTH = B00000000;
  }

  if (Rl & (millis() - LightTime) % 500 < 300) { //right light continue to flash
    //digitalWrite(Rlight, HL);
    PORTH = B00100000;
  } else if (Rl & (millis() - LightTime) % 500 > 300) {
    //digitalWrite(Rlight, !HL);
    PORTH = B00000000;
  }

}

