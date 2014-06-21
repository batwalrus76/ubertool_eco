C
C
C
      SUBROUTINE   ANGTXA
     I                    (XPOS,YPOS,LEN,STR,HV)
C
C     + + + PURPOSE + + +
C     routine to write out character*1 graphics strings
C     one character at a time
C
C     + + + DUMMY ARGUMENTS + + +
      INTEGER     LEN, HV
      REAL        XPOS,YPOS
      CHARACTER*1 STR(LEN)
C
C     + + + ARGUMENT DEFINITIONS + + +
C     XPOS   - x-coordinate of position to start writing string
C     YPOS   - y-coordinate of position to start writing string
C     LEN    - length of character*1 array
C     STR    - character*1 array for graphics output
C     HV     - 1-horizontal lettering,   2- vertical lettering
C
C     + + + LOCAL VARIABLES + + +
      INTEGER     ERRIND,WSID, N, OL
      INTEGER     I,LLEN
      REAL        LXPOS,LYPOS,NXPOS,NYPOS,TXEXPX(4),TXEXPY(4)
C
C     + + + FUNCTIONS + + +
      INTEGER   LENSTR
C
C     + + + INTRINSICS + + +
C     (none)
C
C     + + + EXTERNALS + + +
      EXTERNAL   LENSTR, GTX, GQTXX, GQACWK
C
C     + + + DATA INITIALIZATIONS + + +
C
C     + + + END SPECIFICATIONS + + +
C
C     all other systems except PRIME with DISSPLA use for GKS
C
C     get workstation id
      N = 1
      CALL GQACWK (N,ERRIND,OL,WSID)
C
C     initialize local positions
      LXPOS= XPOS
      LYPOS= YPOS
C     get length of character string
      LLEN = LENSTR (LEN,STR)
      DO 8 I= 1,LLEN
        CALL GTX (LXPOS,LYPOS,STR(I))
C       get next characters coordinates
        CALL GQTXX (WSID,LXPOS,LYPOS,STR(I),
     O              ERRIND,NXPOS,NYPOS,TXEXPX,TXEXPY)
        LXPOS = NXPOS
        LYPOS = NYPOS
 8    CONTINUE
C
      RETURN
      END
C
C
C
      REAL FUNCTION   ANGLEN
     I                       (LEN,CBUF)
C
C     + + + PURPOSE + + +
C     This routine computes the length of a character string in world
C     corrdinates using GKS routines.
C
C     + + + DUMMY ARGUMENTS + + +
      INTEGER   LEN
      CHARACTER*1  CBUF(LEN)
C
C     + + + ARGUMENT DEFINITIONS + + +
C     LEN    - length of character string
C     CBUF   - character string to be plotted
C
C     + + + LOCAL VARIABLES + + +
      INTEGER   I, N, OL
      INTEGER    WSID, ERRIND
      REAL   LXP,LYP,NXPOS,NYPOS,TXEXPX(4),TXEXPY(4)
C
C     + + + EXTERNALS + + +
      EXTERNAL   GQTXX, GQACWK
C
C     + + + END SPECIFICATIONS + + +
C
C     get workstation id
      N = 1
      CALL GQACWK (N,ERRIND,OL,WSID)
C
      LYP = 0.0
      LXP = 0.0
      ANGLEN = 0.0
C     WRITE(FE,*) ' Before and after concatenation points, x then y.'
C
C
      DO 10 I = 1,LEN
        CALL GQTXX (WSID, LXP,LYP, CBUF(I),
     O              ERRIND,NXPOS,NYPOS,TXEXPX,TXEXPY)
C       WRITE(FE,*) LXP,NXPOS,LYP,NYPOS
C
        IF (NXPOS-LXP .GT. NYPOS-LYP) THEN
C         horizontal text
          ANGLEN = NXPOS - LXP + ANGLEN
          LXP = NXPOS
        ELSE
C         vertical text
          ANGLEN = NYPOS - LYP + ANGLEN
          LYP = NYPOS
        END IF
 10   CONTINUE
C
      RETURN
      END
C
C
C
      SUBROUTINE   PRMETA
     M                     (RETCOD)
C
C     + + + PURPOSE + + +
C     This routine does special processing when a DISSPLA meta file
C     is to be the graphics output on the PRIME computer.
C
C     + + + DUMMY ARGUMENTS + + +
      INTEGER   RETCOD
C
C     + + + ARGUMENT DEFINITIONS + + +
C     RETCOD - error code from opening workstation (0-all ok)
C
C     + + + END SPECIFICATIONS + + +
C
      RETURN
      END
C
C
C
      SUBROUTINE   PCGRGT
     O                    (GPAGE,GMODE)
C
C     + + + PURPOSE + + +
C     dummy routine to emulate getting
C     the graphics mode on the PC
C
C     + + + DUMMY ARGUMENTS + + +
      INTEGER   GPAGE,GMODE
C
C     + + + ARGUMENT DEFINITIONS + + +
C     GPAGE - graphics page
C     GMODE - graphics mode
C
C     + + + END SPECIFICATIONS + + +
C
      RETURN
      END
C
C
C
      SUBROUTINE   PCGRST
     I                    (GPAGE,GMODE)
C
C     + + + PURPOSE + + +
C     dummy routine to emulate setting
C     the graphics mode on the PC
C
C     + + + DUMMY ARGUMENTS + + +
      INTEGER   GPAGE,GMODE
C
C     + + + ARGUMENT DEFINITIONS + + +
C     GPAGE - graphics page
C     GMODE - graphics mode
C
C     + + + END SPECIFICATIONS + + +
C
      RETURN
      END
C
Ckmf  commented out gesc for use with gligks Jun 2, 1999
C
Ckmf  SUBROUTINE   GESC
Ckmf I                 (FCTID, LIDR, IDR, MLODR,
Ckmf O                  LODR, ODR)
C
C     + + + PURPOSE + + +
C     Serves as a dummy routine to replace the routine which allows 
C     access to special graphics features specific to PRIOR's implemen-
C     tation of GKS.
C
C     + + + DUMMY ARGUMENTS + + +
Ckmf  INTEGER      FCTID, LIDR, MLODR, LODR
Ckmf  CHARACTER*80 IDR(10), ODR(10)
C
C     + + + ARGUMENT DEFINITIONS + + +
C     FCTID - PRIOR escape function identifier
C     LIDR  - dimension of the input data record array
C     IDR   - input data record
C     MODR  - maximum length of the output data record
C     LODR  - number of array elements occupied in the output data record
C     ODR   - output data record
C
C     + + + END SPECIFICATIONS + + +
C
Ckmf  RETURN
Ckmf  END
C
C
C
      SUBROUTINE   GSFASX
     M                   (PATTRN)
C
C     + + + PURPOSE + + +
C     set pattern after checking for conversion in value assoc with name
C     Oct 2001 - kmf - reordered FILL otions in parmgli.seq
C     so that patterns plotted correspond to the pattern names
C     which use a positive index number.  For now, keep this
C     dummy routine.
C
C     + + + DUMMY ARGUMENTS + + +
      INTEGER   PATTRN
C
C     + + + ARGUMENT DEFINITIONS + + +
C     PATTRN - pattern id number
C
C     + + + END SPECIFICATIONS + + +
C
C     to be replaced summer '94,
C     temp hard code conversions of fill patterns
Ckmf  reordered FILL options in parmgli.seq so that
Ckmf  patterns correspond to order number (positive value).
Ckmf  k
Ckmf  IF (PATTRN.EQ.3) THEN
Ckmf    PATTRN = -1
Ckmf  ELSE IF (PATTRN.EQ.4) THEN
Ckmf    PATTRN = -2
Ckmf  ELSE IF (PATTRN.EQ.5) THEN
Ckmf    PATTRN = -3
Ckmf  ELSE IF (PATTRN.EQ.6) THEN
Ckmf    PATTRN = -4
Ckmf  ELSE IF (PATTRN.EQ.7) THEN
Ckmf    PATTRN = -5
Ckmf  ELSE IF (PATTRN.EQ.8) THEN
Ckmf    PATTRN = -6
Ckmf  END IF
C
      RETURN
      END
C
C
C
      SUBROUTINE   GPREC
     I                  ( IL, IA, RL, RA, SL, LSTR, STR, MLDR,
     O                    ERRIND, LDR, DATREC )
C
C     + + + PURPOSE + + +
C     Serves as a dummy routine to replace the Pack Data Record
C     routine used to put data into the packed format that certain
C     GKS routines need.  (Specifically, used to pack the data
C     record for the Escape routine GESC.  GESC provides for an
C     interface to special features of PRIOR GKS that are not
C     part of the GKS standard.)
C
C     + + + DUMMY ARGUMENTS + + +
      INTEGER   IL, IA(IL), RL, SL, LSTR, MLDR, ERRIND, LDR
      REAL      RA(1)
      CHARACTER*80  DATREC(MLDR), STR
C
C     + + + END SPECIFICATIONS + + +
C
C     do nothing
C
      RETURN
      END