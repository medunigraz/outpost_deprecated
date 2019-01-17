DDL

  CREATE OR REPLACE FORCE EDITIONABLE VIEW ""CO_LOC_API"".""FUNKTIONEN_V"" (""FUNK_NR"", ""FUNK_BEZ"", ""FUNK_NAME_W"", ""FUNK_NAME_M"", ""FUNK_GRUPPE"", ""FUNK_LEITER"") AS 
  select f.NR funk_nr
      ,f.NAME_NEUTRAL funk_bez
      ,f.NAME_WEIBLICH funk_name_w
      ,f.NAME funk_name_m
      ,fg.NAME funk_gruppe
      ,null funk_leiter
from TUG_NEW.FUNKTIONSTYPEN f
    ,tug_new.FUNKTIONSTYP_GRUPPEN fg
where f.FTYP_GRP_NR = fg.NR
  and (f.FTYP_GRP_NR = 1 or f.NR in (6778 -- MEDonline-Beauftragter
                                    ,7828 -- IT-Partner
                                    )
                                    )
  and f.KURZBEZEICHNUNG not in ('ABT_LT','ABT_LT_INT','ABT_LT_SUPP','AKGL_VORS','ETH_VORS','FB_LT','INST_LT'
                               ,'INST_LT_SUPP','KLIN_ABT_LT','KLIN_LT','LT_SUPP','OE_LT','R_BEH_VORS'
                               ,'R_Zentr_Spr','SCHIED_VORS','SEN_VORS_9214','STUDREK','STUKO_VORS','TEACHUNIT_LT'
                               ,'UNIDIR','UNIR_VORS','VREK_9223','REK_9213','BEH_VERTR','BETR_WISS_VOR','BETR_NWISS_VOR'
                               ,'R_DEK_DR','STAB_LT','R_LEHRST','R_LEHRST_SUP','R_LEIT_DF','R_LEIT_DF_SUP','FORS_LT'
                               ,'KLIN_ABT_LT_SUPP','KLIN_LT_SUP','ABT_MANDIR')
  and f.ANZEIGE_FLAG = 'J'
UNION
select f.NR funk_nr
      ,f.NAME_NEUTRAL funk_bez
      ,f.NAME_WEIBLICH funk_name_w
      ,f.NAME funk_name_m
      ,fg.NAME funk_gruppe
      ,'X' funk_leiter
from TUG_NEW.FUNKTIONSTYPEN f
    ,tug_new.FUNKTIONSTYP_GRUPPEN fg
where f.FTYP_GRP_NR = fg.NR
  and (f.FTYP_GRP_NR = 1 or f.NR in (6778 -- MEDonline-Beauftragter
                                    ,7828 -- IT-Partner
                                    )
                                    )
  and f.KURZBEZEICHNUNG in ('ABT_LT','ABT_LT_INT','ABT_LT_SUPP','AKGL_VORS','ETH_VORS','FB_LT','INST_LT'
                            ,'INST_LT_SUPP','KLIN_ABT_LT','KLIN_LT','LT_SUPP','OE_LT','R_BEH_VORS'
                            ,'R_Zentr_Spr','SCHIED_VORS','SEN_VORS_9214','STUDREK','STUKO_VORS','TEACHUNIT_LT'
                            ,'UNIDIR','UNIR_VORS','VREK_9223','REK_9213','BEH_VERTR','BETR_WISS_VOR','BETR_NWISS_VOR'
                            ,'R_DEK_DR','STAB_LT','R_LEHRST','R_LEHRST_SUP','R_LEIT_DF','R_LEIT_DF_SUP','FORS_LT'
                            ,'KLIN_ABT_LT_SUPP','KLIN_LT_SUP','ABT_MANDIR')
  and f.ANZEIGE_FLAG = 'J'

  CREATE OR REPLACE FORCE EDITIONABLE VIEW ""CO_LOC_API"".""GEBAEUDE_V"" (""GEBAEUDE_NR"", ""NAME"", ""KURZBEZEICHNUNG"", ""STRASSE_HAUSNUMMER"") AS 
  select a.NR gebaeude_nr
      ,a.NAME
      ,a.KURZBEZEICHNUNG
      ,b.STRASSE_HAUSNUMMER
from tug_new.GEBAEUDE a
     ,TUG_NEW.adressen b
where a.KURZBEZEICHNUNG like 'MC%'
  and a.ADR_NR = b.NR


  CREATE OR REPLACE FORCE EDITIONABLE VIEW ""CO_LOC_API"".""INT_PROFIL_BILDER_IDS_V"" (""PERSON_NR"", ""DOCUMENT_NR"") AS 
  select pd.PERSON_NR, MAX(pd.DOC_STORE_NR) as DOCUMENT_NR
     from TUG_NEW.personen_documents pd
        , TUG_NEW.person_document_typen pdt
        , TUG_NEW.DOCUMENTS_STORE store
    where pdt.nr = pd.pers_doct_nr
      and pd.DOC_STORE_NR = store.nr
      and pdt.kurzbezeichnung = 'PPO'
      and pd.PERSON_NR is not null
      group by pd.PERSON_NR
      order by pd.PERSON_NR

  CREATE OR REPLACE FORCE EDITIONABLE VIEW ""CO_LOC_API"".""LV_GRP_STUD_V"" (""GRP_NR"", ""STUD_NR"") AS 
  select a.LV_GRP_NR        grp_nr
      ,s.STUD_NR              stud_nr
  FROM TUG_NEW.PU_LV_GRP_PERSONEN_V A
       ,CO_LOC_API.LV_GRP_V gr
       ,co_loc_api.STUD_V s
where a.STATUS_KB = 'FIX'
  and a.LV_GRP_NR = gr.GRP_NR
  and a.ST_PERSON_NR = s.STUD_NR


  CREATE OR REPLACE FORCE EDITIONABLE VIEW ""CO_LOC_API"".""LV_GRP_TERM_V"" (""LV_GRP_NR"", ""PERS_NR"", ""TERMIN_NR"", ""LV_BEGINN"", ""LV_ENDE"", ""LERNEINHEIT"", ""RAUM_NR"", ""RAUM_NUMMER"", ""RAUM_BEZ"", ""GEBAEUDE"", ""STOCKWERK"") AS 
  select te.LV_GRP_NR      lv_grp_nr
      ,te.PERSON_NR      pers_nr
      ,te.TE_TERMIN_NR   termin_nr
      ,te.ZEIT_VON        LV_beginn
      ,te.ZEIT_BIS        lv_ende
      ,t.LERNEINHEIT     Lerneinheit

    --,r.NR              termin_nr
     ,r.RAUM_NR          raum_nr
     ,r.RES_NAME_TEIL1   raum_nummer
     ,r.RES_NAME_TEIL2   raum_bez
     ,ge.NAME            gebaeude
     ,sw.NAME            stockwerk
from TUG_NEW.PU_LV_TERMINE_PRO_PERSON_V te
     ,co_loc_api.LV_GRP_V gr
     ,CO_RESSOURCEN.TE_TERMINE t

    ,CO_RESSOURCEN.PU_TERMINE_RESSOURCEN_V r
    ,tug_new.GEBAEUDE ge
    ,tug_new.STOCKWERK_V sw



where te.EREIGNISTYP_KB = 'A'
  and te.TERMINTYP_KB = 'FT'
  and te.ereignistyp_kb = 'A'
  and te.LV_GRP_NR = gr.GRP_NR
  and te.TE_TERMIN_NR = t.NR

  and te.TE_TERMIN_NR = r.NR
  and substr(r.RES_NAME_TEIL1,1,6) = ge.KURZBEZEICHNUNG
  and substr(r.RES_NAME_TEIL1,7,2) = sw.KURZBEZEICHNUNG
  and nvl(ge.GUELTIG_BIS, TO_DATE('9999/01/01', 'yyyy/mm/dd')) >= sysdate

  CREATE OR REPLACE FORCE EDITIONABLE VIEW ""CO_LOC_API"".""LV_GRP_V"" (""GRP_NR"", ""LV_NR"", ""GRP_NAME"") AS 
  select g.NR          grp_nr
      ,g.STP_SP_NR    lv_nr
      ,g.NAME        grp_name
from tug_new.LV_GRUPPEN g
    ,co_loc_api.LV_V l
 where g.STP_SP_NR = l.LV_NR


  CREATE OR REPLACE FORCE EDITIONABLE VIEW ""CO_LOC_API"".""LV_TERM_RAUM_V"" (""TERMIN_NR"", ""RAUM_NR"", ""RAUM_NUMMER"", ""RAUM_BEZ"", ""GEBAEUDE"", ""STOCKWERK"") AS 
  select r.NR              termin_nr
     ,r.RAUM_NR          raum_nr
     ,r.RES_NAME_TEIL1   raum_nummer
     ,r.RES_NAME_TEIL2   raum_bez
     ,ge.NAME            gebaeude
     ,sw.NAME            stockwerk
from CO_RESSOURCEN.PU_TERMINE_RESSOURCEN_V r
    ,tug_new.GEBAEUDE ge
    ,tug_new.STOCKWERK_V sw
where substr(r.RES_NAME_TEIL1,1,6) = ge.KURZBEZEICHNUNG
  and substr(r.RES_NAME_TEIL1,7,2) = sw.KURZBEZEICHNUNG


  CREATE OR REPLACE FORCE EDITIONABLE VIEW ""CO_LOC_API"".""LV_V"" (""LV_NR"", ""LV_LVNR"", ""LV_TITEL"", ""LV_TYP"", ""LV_TYP_LANG"", ""LV_STUDJAHR"", ""LV_SEMESTER"", ""SEMESTER_BEZEICHNUNG"") AS 
  SELECT s.NR         lv_nr
      ,s.LVNR       lv_lvnr
      ,s.TITEL      lv_titel
      ,sa.NAME_kurz lv_typ
      ,sa.NAME      lv_typ_lang
      ,sj.NAME      lv_studjahr
      ,s.SEMESTER   lv_semester
      ,sem.SEMESTER_BEZEICHNUNG
  FROM tug_new.STP_SEMESTERPLAENE s
       ,tug_new.STP_LV_ARTEN sa
       ,tug_new.PU_STUDIENJAHR_V sj
       ,TUG_NEW.PU_SEMESTER_V sem
where s.STP_LV_ART_NR = sa.NR
  and s.SJ_NR = sj.NR
  and sj.NR = sem.SJ_NR
  and sysdate between sem.SEMESTER_ANFANG and sem.SEMESTER_ENDE
  and sem.SEMESTER_KB = s.SEMESTER


  CREATE OR REPLACE FORCE EDITIONABLE VIEW ""CO_LOC_API"".""MITTEILUNGSBLATT_V"" (""NR"", ""STUDIENJAHR"", ""STUECK"", ""AUSGABEDATUM"", ""ZUSATZ_INFO"", ""LINK"") AS 
  SELECT a.NR
      ,a.STUDIENJAHR
      ,a.STUECK
      ,a.AUSGABEDATUM
      ,a.ZUSATZ_INFO
      ,'https://online.medunigraz.at/mug_online/wbMitteilungsblaetter_neu.display?pNr='||a.NR||'&pDocNr='||a.DOC_NR_PDF||'&pOrgNr='||a.ORG_NR Link
  FROM TUG_NEW.MITTEILUNGSBLAETTER A
  where 		a.PUBLISH = 'J'
  order by a.AUSGABEDATUM desc


  CREATE OR REPLACE FORCE EDITIONABLE VIEW ""CO_LOC_API"".""ORGANISATIONEN_IDS_V"" (""NR"", ""TYP"") AS 
  SELECT --Med Uni Graz
  o1.NR,
  'V' as Typ
from tug_new.ORGANISATIONEN o1
where o1.nr IN (1,      --Medizinische Universität Graz
                14121,  --ORGANE
                23430,  --Kommissionen und Vertretungen
                24247,  --Organisationseinheiten
                24286   --Wissenschaftliche OEs
                )
UNION
SELECT --ORGANE
  o1.NR,
  'OE' as Typ
from tug_new.ORGANISATIONEN o1
where sysdate between o1.GUELTIG_AB and (nvl(o1.GUELTIG_BIS,sysdate + 1))
  and o1.nr in (select o.nr
                      from tug_new.ORGANISATIONEN o
                     where sysdate between o.GUELTIG_AB and (nvl(o.GUELTIG_BIS,sysdate + 1))
                    CONNECT BY PRIOR o.nr = o.org_nr
                     START WITH o.org_nr = 14121)
UNION
SELECT --Kommisionen und Vertretungen
  o1.NR,
  'OE' as Typ
from tug_new.ORGANISATIONEN o1
where sysdate between o1.GUELTIG_AB and (nvl(o1.GUELTIG_BIS,sysdate + 1))
  and o1.nr in (select o.nr
                      from tug_new.ORGANISATIONEN o
                     where sysdate between o.GUELTIG_AB and (nvl(o.GUELTIG_BIS,sysdate + 1))
                    CONNECT BY PRIOR o.nr = o.org_nr
                     START WITH o.org_nr = 23430)
UNION
select
  o.NR,
  CASE o.ORG_TYP_NR 
   WHEN 32974 THEN 'TU'
   WHEN 32973 THEN 'FE'
   ELSE 'OE' END as Typ
  from tug_new.ORGANISATIONEN_T o
  where 
    --o.ORG_TYP_NR not in (32973, 32974) --Forschungseinheiten/Teaching Units
    --AND 
    sysdate between o.GUELTIG_AB and (nvl(o.GUELTIG_BIS, sysdate + 1))
    CONNECT BY PRIOR o.nr = o.org_nr
    START WITH o.org_nr = 24286

  CREATE OR REPLACE FORCE EDITIONABLE VIEW ""CO_LOC_API"".""ORGANISATIONEN_V"" (""NR"", ""NAME_KURZ"", ""ORG_NAME"", ""BASISORGANISATION"", ""TYP"", ""ADRESSE"", ""EMAIL_ADRESSE"", ""TELEFON_NUMMER"", ""WWW_HOMEPAGE"", ""SORT_HIERARCHIE"") AS 
  Select
  o.NR as NR,
  o.NAME_KURZ as NAME_KURZ,
  REPLACE(REPLACE(REPLACE(REPLACE(o.NAME, '""', ''), '„', ''), '“', ''), '&', '') org_name,
  o.ORG_NR as BasisOrganisation,
  v.TYP,
  a.adresse, a.email_adresse, a.telefon_nummer, a.www_homepage,
  o.SORT_HIERARCHIE
from ORGANISATIONEN_IDS_V v, tug_new.ORGANISATIONEN o, TUG_NEW.PU_ORG_ADR_V a
where o.nr = v.nr
      and a.nr(+) = o.nr
order by o.SORT_HIERARCHIE

  CREATE OR REPLACE FORCE EDITIONABLE VIEW ""CO_LOC_API"".""PERSONEN_ORGANISATIONEN_V"" (""PERSON_NR"", ""ORG_NR"", ""PERS_FAMNAM"", ""PERS_VORNAME"") AS 
  select 
        DISTINCT
        p.PERS_NR person_nr
       ,po.ORG_NR
       ,p.PERS_FAMNAM
       ,p.PERS_VORNAME
  from PERSON_V p
      ,tug_new.personen_organisationen po
      ,tug_new.FUNKTIONEN_DIENSTEIGENSCHAFTEN fd
      ,ORGANISATIONEN_IDS_V org
where
  p.PERS_NR = po.PERSON_NR
  and po.FUNK_DE_NR = fd.NR
  and trunc(po.BEGINN_DATUM) < trunc(sysdate)
  and trunc(nvl(po.ENDE_DATUM,sysdate)) >= sysdate-1
  and fd.FU_DE_TYP = 'D'
  and org.NR = po.ORG_NR 
  --and po.ORG_NR in (Select nr from ORGANISATIONEN_IDS_V)
  --and fd.DE_GRP_NR = 2
  --and fd.DE_KURZBEZEICHNUNG not in ('PR','LKH','CBMED')
  

  CREATE OR REPLACE FORCE EDITIONABLE VIEW ""CO_LOC_API"".""PERSONEN_PROFILBILDER_DATEN_V"" (""PERSON_NR"", ""CONTENT"") AS 
  select pr.PERSON_NR, store.CONTENT
   from INT_PROFIL_BILDER_IDS_V pr
      , TUG_NEW.DOCUMENTS_STORE store
  where pr.DOCUMENT_NR = store.nr

  CREATE OR REPLACE FORCE EDITIONABLE VIEW ""CO_LOC_API"".""PERSONEN_RAUM_ALLE_V"" (""NR"", ""VORNAME"", ""FAMILIENNAME"", ""TITEL"", ""RAUM_NR"") AS 
  SELECT DISTINCT pers.nr, pers.VORNAME, pers.FAMILIENNAME, pers.TITEL, MIN(ort.raum_nr) as raum_nr
FROM 
  TUG_NEW.PERS_DIENSTORTE_VK_V ort,
  TUG_NEW.PU_PERSONEN_V pers
WHERE
  ort.PERSON_NR = pers.NR
  and ort.raum_nr is not null
GROUP BY pers.nr, pers.VORNAME, pers.FAMILIENNAME, pers.TITEL

  CREATE OR REPLACE FORCE EDITIONABLE VIEW ""CO_LOC_API"".""PERSONEN_RAUM_V"" (""NR"", ""VORNAME"", ""FAMILIENNAME"", ""TITEL"", ""RAUM_NR"", ""RAUM_BEZ"", ""GEBAEUDE_NR"", ""GEBAEUDE"", ""STOCKWERK_NR"", ""STOCKWERK"", ""RAUM"", ""RAUM_NUMMER"", ""FLAECHE"", ""HOEHE"", ""ORG_NR"", ""ORGANISATION"", ""RAUMTYP"") AS 
  SELECT DISTINCT 
       p.NR,
       p.VORNAME,
       p.FAMILIENNAME,
       p.TITEL,
       p.RAUM_NR,
       v.RAUM_BEZ,
       v.GEBAEUDE_NR,
       v.GEBAEUDE,
       v.STOCKWERK_NR,
       v.STOCKWERK,
       v.RAUM,
       v.RAUM_NUMMER,
       v.FLAECHE,
       v.HOEHE,
       v.ORG_NR,
       v.ORGANISATION,
       v.RAUMTYP
FROM CO_LOC_API.PERSONEN_RAUM_ALLE_V p, CO_LOC_API.RAUM_V v where v.RAUM_NR = p.RAUM_NR

  CREATE OR REPLACE FORCE EDITIONABLE VIEW ""CO_LOC_API"".""PERSON_I_V"" (""PERS_NR"", ""PERS_FAMNAM"", ""PERS_VORNAME"", ""PERS_TITEL"", ""PERS_SEX"", ""PERS_BENUTZERNAME"", ""PERS_SPRECHSTUNDE"", ""PERS_ZUSATZ_INFO"", ""PERS_PROFILBILD"", ""PERS_EMAIL"") AS 
  select DISTINCT  
      p.nr           pers_nr
      ,p.FAMILIENNAME pers_famnam
      ,p.VORNAME      pers_vorname
      ,tug_new.pupers.GETTITEL(p.NR) pers_titel
      ,p.GESCHLECHT pers_sex
      ,bk.BENUTZERNAME pers_benutzername
      ,p.SPRECHSTUNDE pers_sprechstunde
      ,p.zusatz_info pers_zusatz_info
      ,'https://online.medunigraz.at/mug_online/visitenkarte.showImage?pPersonenGruppe='|| 
          TUG_NEW.PUIDENT.PERSGRUPPEBEDIENSTETE() || 
          CHR(38) ||
          'pPersonenId=' ||
          p.NR_OBFUSCATED as pers_profilbild
      , TUG_NEW.PUPERS.GETEMAIL(p.nr) pers_email
from tug_new.PERSONEN p
     ,co_sec.BENUTZER_KONTEN bk
     ,tug_new.personen_organisationen po
where p.NR = bk.PERSON_NR
  and bk.KTOSTTYP_NR = 1
  and bk.BGRUPPE_NR = 2
  and p.NR = po.PERSON_NR
  and trunc(po.BEGINN_DATUM) < trunc(sysdate)
  and trunc(nvl(po.ENDE_DATUM,sysdate)) >= sysdate-1
  and p.REALE_PERSON_FLAG = 'J' -- Sollen die Testuser dabei sein

  CREATE OR REPLACE FORCE EDITIONABLE VIEW ""CO_LOC_API"".""PERSON_V"" (""PERS_NR"", ""PERS_FAMNAM"", ""PERS_VORNAME"", ""PERS_TITEL"", ""PERS_SEX"", ""PERS_BENUTZERNAME"", ""PERS_SPRECHSTUNDE"", ""PERS_ZUSATZ_INFO"", ""PERS_PROFILBILD"", ""RAUM_NR"", ""PERS_EMAIL"") AS 
  Select p.pers_nr, 
        p.pers_famnam,
        p.pers_vorname,
        p.pers_titel,
        p.pers_sex,
        p.pers_benutzername,
        p.pers_sprechstunde,
        p.pers_zusatz_info,
        p.pers_profilbild,
        MIN(ort.raum_nr) raum_nr,
        p.pers_email
from PERSON_I_V p, TUG_NEW.PERS_DIENSTORTE_VK_V ort
WHERE
  ort.PERSON_NR(+) = p.PERS_NR
GROUP BY p.pers_nr, 
        p.pers_famnam,
        p.pers_vorname,
        p.pers_titel,
        p.pers_sex,
        p.pers_benutzername,
        p.pers_sprechstunde,
        p.pers_zusatz_info,
        p.pers_profilbild,
        p.pers_email

  CREATE OR REPLACE FORCE EDITIONABLE VIEW ""CO_LOC_API"".""PERS_ORG_FUNK_V"" (""PERS_NR"", ""ORG_NR"", ""FUNK_NR"") AS 
  select DISTINCT po.PERSON_NR pers_nr
      ,po.ORG_NR org_nr
      ,f.FUNK_NR funk_nr
from TUG_NEW.PERSONEN_ORGANISATIONEN po
    ,co_loc_api.PERSON_V p
    ,tug_new.FUNKTIONEN_DIENSTEIGENSCHAFTEN fd
    ,co_loc_api.FUNKTIONEN_V f
where po.PERSON_NR = p.PERS_NR
  and sysdate between po.BEGINN_DATUM and nvl(po.ENDE_DATUM,sysdate+1)
  and po.FUNK_DE_NR = fd.NR
  and fd.FU_DE_TYP = 'F'
  and fd.FUNKTYP_NR = f.FUNK_NR

  CREATE OR REPLACE FORCE EDITIONABLE VIEW ""CO_LOC_API"".""RAUM_TYPEN_V"" (""NR"", ""NAME_DE"", ""NAME_EN"") AS 
  SELECT 
    rt.nr NR, rt.name.de NAME_DE, rt.name.en NAME_EN
FROM 
    tug_new.Raum_typen_lt rt

  CREATE OR REPLACE FORCE EDITIONABLE VIEW ""CO_LOC_API"".""RAUM_V"" (""RAUM_NR"", ""RAUM_BEZ"", ""GEBAEUDE_NR"", ""GEBAEUDE"", ""STOCKWERK_NR"", ""STOCKWERK"", ""RAUM"", ""RAUM_NUMMER"", ""FLAECHE"", ""HOEHE"", ""ORG_NR"", ""ORGANISATION"", ""RAUMTYP"") AS 
  select r.nr Raum_nr
     , nvl(r.zusatzbezeichnung, tug_new.puraum.getname(r.nr)) raum_bez
     , g.NR gebaeude_nr
     , g.kurzbezeichnung Gebaeude
     , s.NR stockwerk_nr
     , s.anzeige_kb_fixe_laenge Stockwerk
     , r.RAUM_NR raum
     , g.kurzbezeichnung||s.anzeige_kb_fixe_laenge||r.raum_nr Raum_nummer
     ,r.FLAECHE
     ,r.HOEHE
     ,o.NR org_nr
     ,o.NAME Organisation
     ,rt.NR Raumtyp
  from tug_new.gebaeude g
     , tug_new.stockwerktypen_stkw_fv s
     , tug_new.gut_typen gt
     , tug_new.raeume r
     , tug_new.organisationen_raeume   o_r
     , tug_new.organisationen o
     , tug_new.Raum_typen_lt rt
  where r.nr = o_r.raum_nr
   and o_r.verwalter_flag  = 'J'
   and o_r.ORG_NR = o.NR
   and sysdate between o_r.von and nvl(o_r.bis,sysdate)
   and s.nr = r.geb_stkw_stkwtyp_nr
   and g.nr = r.geb_stkw_geb_nr
   and r.gut_typ_nr = gt.nr
--   and g.KURZBEZEICHNUNG like 'MC%'
   and gt.RAUM_TYP_NR = rt.NR

  CREATE OR REPLACE FORCE EDITIONABLE VIEW ""CO_LOC_API"".""STOCKWERK_V"" (""NR"", ""KURZBEZEICHNUNG"", ""NAME"") AS 
  select b.NR,b.KURZBEZEICHNUNG,b.NAME
from tug_new.STOCKWERKTYP_FILTER a
    ,tug_new.STOCKWERKTYPEN b
where a.STKWTYP_NR = b.NR


  CREATE OR REPLACE FORCE EDITIONABLE VIEW ""CO_LOC_API"".""STUD_V"" (""STUD_NR"", ""STUD_MNR"", ""STUD_FAMNAM"", ""STUD_VORNAME"", ""STUD_AKADGRAD"", ""STUD_SEX"", ""STUD_MIFARE"") AS 
  select distinct 
      sp.NR               stud_nr
      ,sp.MATRIKELNUMMER  stud_mnr
      ,sp.FAMILIENNAME    stud_famnam
      ,sp.VORNAME         stud_vorname
      ,sp.AKADGRAD        stud_akadgrad
      ,sp.GESCHLECHT      stud_sex
      --,st.STUDIDF         stud_studium
      ,uc.MIFARE_ID       stud_mifare
  FROM stud.ST_PERSONEN sp
       ,STUD.PU_STUDIEN_V st
       ,unicard.UNICARDS uc
where sp.NR = st.ST_PERSON_NR
  and st.STATUS in ('I','U','o','a','B','E')
  and sp.NR = uc.ST_PERSON_NR(+)
  and uc.STATUS(+) = 'A'

  CREATE OR REPLACE FORCE EDITIONABLE VIEW ""CO_LOC_API"".""VERANSTALTUNGEN_HEUTE_V"" (""PK_INTWB"", ""PK_LV"", ""PK_VERANST"", ""REIHUNG"", ""TYP"", ""NUMMER"", ""TITEL"", ""DATUM"", ""ZEIT_VON"", ""ZEIT_BIS"", ""PK_GEB"", ""GEBAEUDE"", ""PK_RAUM"", ""RAUM"", ""RAUM_BEZ"", ""TERMINART"", ""ANZEIGE_BIS"") AS 
  select k.NR pk_intwb
      ,null pk_lv
      ,null pk_veranst
      ,1 Reihung
      ,'Interne Weiterbildung' typ
      ,k.NUMMER nummer
      ,k.TITEL titel
--      ,case when k.PERSON_NR is not null
--              then p.FAMILIENNAME||' '||p.VORNAME
--            when k.EXT_PERS_NR is not null
--              then ep.NACHNAME||' '||ep.VORNAME
--            when k.wb_externe_nr is not null
--              then wep.NACHNAME||' '||wep.VORNAME
--             else 'Unbekannt'
--        end vortragender
      ,t.datum_am datum
      ,t.ZEIT_VON zeit_von
      ,t.ZEIT_BIS zeit_bis
      ,g.nr pk_geb
      ,r.gebaeude_kb gebaeude
      ,r.nr pk_raum
      ,r.code raum
      ,r.zusatzbezeichnung raum_bez
      ,st.name.de Terminart
    -- anzeigen bis von-zeit plus 20 minuten:
      ,to_date( to_char( t.datum_am, 'dd.mm.yyyy ')||to_char( t.zeit_von, 'hh24:mi'), 'dd.mm.yyyy hh24:mi') + 30/1440 anzeige_bis
from tug_wb.WB_KURSE k
    ,tug_new.te_TERMINE t
--    ,tug_new.personen p
--    ,tug_new.EXTERNE_PERSONEN ep
--    ,tug_wb.WB_EXTERNE wep
    ,tug_new.PU_TE_RAEUME_V r
    ,tug_new.gebaeude g
    ,tug_wb.WB_KURS_STATI_LT st
where k.WB_KURS_ST_NR in (2,3)
  and k.NR = t.WB_KURS_NR
  and k.WB_KURS_ST_NR = st.NR
--  and t.DATUM_AM between sysdate - 1 and sysdate + 20
    and trunc(t.DATUM_AM) = trunc(sysdate)
--  and nvl(k.PERSON_NR,999999) = p.NR (+)
--  and nvl(k.EXT_PERS_NR,999999) = ep.NR (+)
--  and nvl(k.WB_EXTERNE_NR,999999) = wep.NR (+)
  and nvl(t.TE_RES_NR,999999) = r.RES_NR (+)
  and r.GEBAEUDE_KB = g.KURZBEZEICHNUNG
UNION
-- LV
select null pk_intwb
      ,s.NR pk_lv
      ,null pk_veranst
      ,3 Reihung
      ,'Lehrveranstaltung' typ
      ,decode(l.ART_KB,'PT','Prüfung',substr(s.LVNR,1,4)||'.'||substr(s.LVNR,5,3)) nummer
      ,s.TITEL titel
--      ,p.FAMILIENNAME||' '||p.VORNAME vortragender
      ,l.TERMIN_DATUM_AM datum
      ,l.TERMIN_ZEIT_VON zeit_von
      ,l.TERMIN_ZEIT_BIS zeit_bis
      ,g.NR pk_geb
      ,r.gebaeude_kb gebaeude
      ,r.NR pk_raum
      ,r.code raum
      ,r.zusatzbezeichnung raum_bez
      ,decode(l.TERMIN_TYP_KB,'FT','fix'
                             ,'FA','abgesagt'
                             ,'FV','verschoben') Terminart
    -- anzeigen bis von-zeit plus 20 minuten:
      ,to_date( to_char( l.TERMIN_DATUM_AM, 'dd.mm.yyyy ')||to_char( l.TERMIN_ZEIT_VON, 'hh24:mi'), 'dd.mm.yyyy hh24:mi') + 30/1440 anzeige_bis
from  tug_new.STP_SEMESTERPLAENE s
     ,TUG_NEW.PU_LV_TE_RESOURCEN_V l
     ,tug_new.PU_TE_RAEUME_V r
     ,tug_new.GEBAEUDE g
--     ,TUG_NEW.LV_GRP_VORTR_V v
--     ,tug_new.personen p
where --l.TERMIN_DATUM_AM between sysdate - 1 and sysdate + 20
     trunc(l.TERMIN_DATUM_AM) = trunc(sysdate)
  and l.STP_SP_NR = s.NR
  and l.TE_RES_NR = r.RES_NR
  and l.TERMIN_TYP_KB in ('FT','FA')  -- absichtlich ohne Verschobene   ,'FV')
  and l.ART_KB not in ('AV','N')
  and r.GEBAEUDE_KB = g.KURZBEZEICHNUNG
--  and l.LV_GRP_NR = v.LV_GRP_NR
--  and v.VORTR_PERSON_NR = p.nr
-- Veranstaltungen
UNION
select null pk_intwb
      ,null pk_lv
      ,v.NR pk_veranst
      ,2 Reihung
      ,'Veranstaltung' typ
      ,v.VA_ART_NAME nummer
      ,v.TITEL titel
--      ,p.FAMILIENNAME||' '||p.VORNAME vortragender
      ,t.datum_am datum
      ,t.ZEIT_VON zeit_von
      ,t.ZEIT_BIS zeit_bis
      ,g.NR pk_geb
      ,r.gebaeude_kb gebaeude
      ,r.NR pk_raum
      ,r.code raum
      ,r.zusatzbezeichnung raum_bez
     -- ,'fix' Terminart
      ,decode(v.ABGESAGT_FLAG,'N','fix'
                             ,'abgesagt') Terminart
    -- anzeigen bis von-zeit plus 20 minuten:
      ,to_date( to_char( t.datum_am, 'dd.mm.yyyy ')||to_char( t.ZEIT_VON, 'hh24:mi'), 'dd.mm.yyyy hh24:mi') + 30/1440 anzeige_bis
from tug_new.pu_va_veranstaltungen

  CREATE OR REPLACE FORCE EDITIONABLE VIEW ""CO_LOC_API"".""VERTEILERLISTE_PERSON_V"" (""PROFIL_NR"", ""PERS_NR"", ""PERS_BENUTZERNAME"") AS 
  select
        vtl.profil_nr,
        vtl.pers_nr,
        ko.benutzername pers_benutzername
    from
         tug_new.loc_mug_verteilerlisten vtl
       , co_sec.benutzer_konten_v        ko 
    where
        vtl.pers_nr = ko.person_nr
      and ko.bengruppen_kb = 'B'
      and ko.konto_status  = 'OK'
      and exists (select null
                    from tug_New.personen_organisationen po
                   where po.person_nr = ko.person_nr
                     and trunc(po.beginn_datum) < trunc(sysdate)
                     and trunc(nvl(po.ende_datum,sysdate)) >= sysdate-1)

  CREATE OR REPLACE FORCE EDITIONABLE VIEW ""CO_LOC_API"".""VERTEILERLISTE_V"" (""PROFIL_NR"", ""PROFIL_NAME"") AS 
  SELECT DISTINCT
        vte.profil_nr,
        b.profil_name
    FROM
        TUG_NEW.LOC_MUG_VERTEILERLISTEN vte
        JOIN tug_new.b_profile b ON b.nr = vte.profil_nr
