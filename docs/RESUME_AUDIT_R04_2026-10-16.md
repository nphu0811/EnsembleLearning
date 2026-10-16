# RESEARCH LOOP r04 — kết quả và checkpoint

Đã đọc MASTER_PROMPT/AGENTS và memory, tiếp tục r03 không restart. Entry audit174/174 prior hashes khớp,282/282 historical files nguyên,ZIP15entries vàDOCX8tables CRC PASS. Raw,source training,frozen configs/results vàtemplates/original không sửa. Evidence entry: results/reproducibility/resume_2026_10_16_r04/resume_audit.json. Task checkpoints riêng trong .research_memory/r04/.

## Các task đã thực thi

1. R04-REF:6fresh Crossref DOI responses200;5/6 pending entries mới verified;current11/12. L03 giữCHECK_SUGGESTED do254–262/254–263 conflict,không tựxácnhận. U01/U03 vẫnwarning. Metadata/source/reading boundaries tại literature/resume_r04_2026_10_16/;validation28/28. Không whole-paper/systematic-review completion.
2. R04-READ:source-linked selected passages L06,L09,L03 documentation,D01/D02;10/10capture checks. Source map/notes chỉghiđoạnđãđọc;khôngmangCICerrors sangUNSW hoặcnhậpmetric khácprotocol.
3. R04-GAP-LIT:gap matrix theoRQ vàluậncứ/tổngquan trong/ngoàinước. Haiindependentpartialreviews đãlưu;P2provenance/bridge/spacing được sửa.30/30source/RQ checks,3/3repair checks. Reviewer judgment khôngartifact/phasecompletion.
4. R04-FORM-AUDIT:đọc toànDOCX read-only,58blocks và97cells;coverage14/14. Bảnggốc,ngânsách,lịch,copies,chữký giữmapping vàpendingfields. Không filled/renderedDOCX.
5. R04-ASSEMBLY:ghép nội dung theoform;10/10initialchecks,6/6P2repairchecks. Evidencefull-contentreportđãlưu;argumentfull-contentreview khôngcófiledoagentusage limit. TrạngtháiPARTIAL,khôngfullproposalapproval. RootđọcreportthậtvàsửafindingsC15/namespace/metadata display.
6. R04-ML-SMOKE:freshvenv actualpipinstall/pipcheck;3frozenbuildersfit2.000TRAINrows,500TRAINvalidation. First41/42failbitwiseRF17;diagnosisparallelfloating-point2.22e-16;preservefailure. Numeric1e-12+exactlabelsrepair→45/45. NoofficialTESTCSVread,no tuning,no scientificmetric.3modelartifactsSMOKE_ONLYkhôngfinalmodel/demo.6/6historicalauditunittestsPASS. Report docs/research/R04_ML_SMOKE_REPORT.md.
7. R04-DEFENSE-CONTENT:kịchbản12positions720seconds,runbook,checklist;25/25source/timingchecks. ChưaPPTX/PDF/render/rehearsal/finalinference.

## Những lỗi và giới hạn đã ghi thật

- arXivpreflightTLSfail;Crossref/PubMedOK. Publisher403/429/robotchecks giữsourcecaptures;khôngbypass.
- FirstliteraturevalidatorregexkhôngmatchRQheading→sửa parserthật,kiểmparse+exactwording5RQs;khônggọi20checksbanđầuđãkiểmRQđủ. Final30checksghiđúng.
- CheckpointFORMfirstrejectundeclaredgapchange→khôngsilentrefresh;khai báo workinggapdraft vàcheckpointthànhcông.
- Fullcontentargumentreviewusage limit;fileevidencereviewcótrênđĩanhưngagentkếtthúcquota. Khônginventreviewcompletion;khônglấypartialreviewthayfull.
- Smokeinitialexit1;diagnostic vàrerun giữthưmục riêng. Khôngsửa frozen scientific outputsđểkhớp.

## Release gates

G0/G1/G2PARTIAL vớigiới hạn đãghi;G3PARTIAL,cóthêmsoftwareTRAINsmokechưafullreconstruction;G4BLOCKEDfinalreport/render/referenceclosure;G5AUTHOR_INPUT_NEEDED vàDOCX/PDFchưarender;G6NOT_READY(slides/finaldemo/rehearsal). KhôngFINAL_NCKH.zip. Chi tiết hiện hành release/RELEASE_BLOCKERS.md.

## Lệnh/task đầu phiên sau

ĐọcHANDOFF/STATE rồi`python tools/resume_checkpoint_audit.py --out-dir results/reproducibility/NEXT_UNIQUE_SESSION`. Sauhashcheck,ưu tiêncompleteindependentargument/formreview cho`proposal/researchwrite/nckh-ids/drafts/De_cuong_noi_dung_review_r04.md`;khôngrerunexperiment/smokeđãPASSchỉđểđổistatus. L03/U01/U03 chỉđóngkhicóprimaryevidencemới. CóthểtiếptụcP16/report source/finalmodelreconstructiontheocontractriêng khiđủnguồn lực. Chưaoriginalenv/finalmodel; khôngdùngSMOKE_ONLYlàmdemo.

Phiên chạm giới hạn năng lực reviewer độc lập; đã làm tiếp các task độc lập và lưu trạng thái trước kết thúc. Không có background jobs. Exact artifact manifests/task JSON và post-audit là bằng chứng số lượng/checks cuối, không suy từ tên file.
