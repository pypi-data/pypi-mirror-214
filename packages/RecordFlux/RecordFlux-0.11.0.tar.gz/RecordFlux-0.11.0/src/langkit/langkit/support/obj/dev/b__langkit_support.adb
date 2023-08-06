pragma Warnings (Off);
pragma Ada_95;
pragma Source_File_Name (langkit_supportmain, Spec_File_Name => "b__langkit_support.ads");
pragma Source_File_Name (langkit_supportmain, Body_File_Name => "b__langkit_support.adb");
pragma Suppress (Overflow_Check);
with Ada.Exceptions;

package body langkit_supportmain is

   E154 : Short_Integer; pragma Import (Ada, E154, "system__os_lib_E");
   E093 : Short_Integer; pragma Import (Ada, E093, "ada__exceptions_E");
   E089 : Short_Integer; pragma Import (Ada, E089, "system__soft_links_E");
   E087 : Short_Integer; pragma Import (Ada, E087, "system__exception_table_E");
   E120 : Short_Integer; pragma Import (Ada, E120, "ada__containers_E");
   E149 : Short_Integer; pragma Import (Ada, E149, "ada__io_exceptions_E");
   E102 : Short_Integer; pragma Import (Ada, E102, "ada__numerics_E");
   E084 : Short_Integer; pragma Import (Ada, E084, "ada__strings_E");
   E138 : Short_Integer; pragma Import (Ada, E138, "ada__strings__maps_E");
   E141 : Short_Integer; pragma Import (Ada, E141, "ada__strings__maps__constants_E");
   E125 : Short_Integer; pragma Import (Ada, E125, "interfaces__c_E");
   E096 : Short_Integer; pragma Import (Ada, E096, "system__exceptions_E");
   E163 : Short_Integer; pragma Import (Ada, E163, "system__object_reader_E");
   E132 : Short_Integer; pragma Import (Ada, E132, "system__dwarf_lines_E");
   E177 : Short_Integer; pragma Import (Ada, E177, "system__soft_links__initialize_E");
   E119 : Short_Integer; pragma Import (Ada, E119, "system__traceback__symbolic_E");
   E101 : Short_Integer; pragma Import (Ada, E101, "system__img_int_E");
   E144 : Short_Integer; pragma Import (Ada, E144, "system__img_uns_E");
   E217 : Short_Integer; pragma Import (Ada, E217, "ada__assertions_E");
   E181 : Short_Integer; pragma Import (Ada, E181, "ada__strings__utf_encoding_E");
   E187 : Short_Integer; pragma Import (Ada, E187, "ada__tags_E");
   E083 : Short_Integer; pragma Import (Ada, E083, "ada__strings__text_buffers_E");
   E258 : Short_Integer; pragma Import (Ada, E258, "gnat_E");
   E213 : Short_Integer; pragma Import (Ada, E213, "interfaces__c__strings_E");
   E195 : Short_Integer; pragma Import (Ada, E195, "ada__streams_E");
   E207 : Short_Integer; pragma Import (Ada, E207, "system__file_control_block_E");
   E206 : Short_Integer; pragma Import (Ada, E206, "system__finalization_root_E");
   E204 : Short_Integer; pragma Import (Ada, E204, "ada__finalization_E");
   E203 : Short_Integer; pragma Import (Ada, E203, "system__file_io_E");
   E322 : Short_Integer; pragma Import (Ada, E322, "system__regpat_E");
   E275 : Short_Integer; pragma Import (Ada, E275, "system__storage_pools_E");
   E277 : Short_Integer; pragma Import (Ada, E277, "system__finalization_masters_E");
   E298 : Short_Integer; pragma Import (Ada, E298, "system__storage_pools__subpools_E");
   E227 : Short_Integer; pragma Import (Ada, E227, "ada__strings__unbounded_E");
   E422 : Short_Integer; pragma Import (Ada, E422, "ada__strings__wide_wide_maps_E");
   E418 : Short_Integer; pragma Import (Ada, E418, "ada__strings__wide_wide_unbounded_E");
   E219 : Short_Integer; pragma Import (Ada, E219, "ada__calendar_E");
   E407 : Short_Integer; pragma Import (Ada, E407, "ada__calendar__delays_E");
   E306 : Short_Integer; pragma Import (Ada, E306, "ada__calendar__time_zones_E");
   E193 : Short_Integer; pragma Import (Ada, E193, "ada__text_io_E");
   E403 : Short_Integer; pragma Import (Ada, E403, "gnat__byte_order_mark_E");
   E311 : Short_Integer; pragma Import (Ada, E311, "gnat__calendar_E");
   E375 : Short_Integer; pragma Import (Ada, E375, "gnat__directory_operations_E");
   E339 : Short_Integer; pragma Import (Ada, E339, "system__checked_pools_E");
   E279 : Short_Integer; pragma Import (Ada, E279, "system__pool_global_E");
   E357 : Short_Integer; pragma Import (Ada, E357, "gnat__expect_E");
   E399 : Short_Integer; pragma Import (Ada, E399, "system__random_seed_E");
   E386 : Short_Integer; pragma Import (Ada, E386, "system__regexp_E");
   E379 : Short_Integer; pragma Import (Ada, E379, "ada__directories_E");
   E316 : Short_Integer; pragma Import (Ada, E316, "system__img_lli_E");
   E318 : Short_Integer; pragma Import (Ada, E318, "system__img_llu_E");
   E314 : Short_Integer; pragma Import (Ada, E314, "gnat__calendar__time_io_E");
   E328 : Short_Integer; pragma Import (Ada, E328, "gnat__debug_pools_E");
   E415 : Short_Integer; pragma Import (Ada, E415, "gnatcoll__gmp__integers_E");
   E028 : Short_Integer; pragma Import (Ada, E028, "langkit_support__errors_E");
   E243 : Short_Integer; pragma Import (Ada, E243, "adasat_E");
   E254 : Short_Integer; pragma Import (Ada, E254, "adasat__decisions_E");
   E251 : Short_Integer; pragma Import (Ada, E251, "adasat__vectors_E");
   E249 : Short_Integer; pragma Import (Ada, E249, "adasat__formulas_E");
   E252 : Short_Integer; pragma Import (Ada, E252, "adasat__internals_E");
   E245 : Short_Integer; pragma Import (Ada, E245, "adasat__builders_E");
   E256 : Short_Integer; pragma Import (Ada, E256, "adasat__dpll_E");
   E266 : Short_Integer; pragma Import (Ada, E266, "gnatcoll__atomic_E");
   E326 : Short_Integer; pragma Import (Ada, E326, "gnatcoll__memory_E");
   E353 : Short_Integer; pragma Import (Ada, E353, "gnatcoll__os_E");
   E272 : Short_Integer; pragma Import (Ada, E272, "gnatcoll__storage_pools__headers_E");
   E270 : Short_Integer; pragma Import (Ada, E270, "gnatcoll__refcount_E");
   E352 : Short_Integer; pragma Import (Ada, E352, "gnatcoll__string_builders_E");
   E268 : Short_Integer; pragma Import (Ada, E268, "gnatcoll__strings_impl_E");
   E264 : Short_Integer; pragma Import (Ada, E264, "gnatcoll__strings_E");
   E263 : Short_Integer; pragma Import (Ada, E263, "gnatcoll__strings_E");
   E341 : Short_Integer; pragma Import (Ada, E341, "gnatcoll__mmap_E");
   E343 : Short_Integer; pragma Import (Ada, E343, "gnatcoll__mmap__system_E");
   E346 : Short_Integer; pragma Import (Ada, E346, "gnatcoll__templates_E");
   E348 : Short_Integer; pragma Import (Ada, E348, "gnatcoll__terminal_E");
   E350 : Short_Integer; pragma Import (Ada, E350, "gnatcoll__utils_E");
   E370 : Short_Integer; pragma Import (Ada, E370, "gnatcoll__io_E");
   E388 : Short_Integer; pragma Import (Ada, E388, "gnatcoll__path_E");
   E377 : Short_Integer; pragma Import (Ada, E377, "gnatcoll__io__native_E");
   E391 : Short_Integer; pragma Import (Ada, E391, "gnatcoll__remote_E");
   E395 : Short_Integer; pragma Import (Ada, E395, "gnatcoll__remote__db_E");
   E373 : Short_Integer; pragma Import (Ada, E373, "gnatcoll__io__remote_E");
   E390 : Short_Integer; pragma Import (Ada, E390, "gnatcoll__io__remote__unix_E");
   E393 : Short_Integer; pragma Import (Ada, E393, "gnatcoll__io__remote__windows_E");
   E362 : Short_Integer; pragma Import (Ada, E362, "gnatcoll__vfs_E");
   E302 : Short_Integer; pragma Import (Ada, E302, "gnatcoll__traces_E");
   E405 : Short_Integer; pragma Import (Ada, E405, "gnatcoll__iconv_E");
   E013 : Short_Integer; pragma Import (Ada, E013, "langkit_support__adalog_E");
   E002 : Short_Integer; pragma Import (Ada, E002, "langkit_support__adalog__debug_E");
   E006 : Short_Integer; pragma Import (Ada, E006, "langkit_support__adalog__logic_var_E");
   E012 : Short_Integer; pragma Import (Ada, E012, "langkit_support__adalog__solver_interface_E");
   E015 : Short_Integer; pragma Import (Ada, E015, "langkit_support__array_utils_E");
   E017 : Short_Integer; pragma Import (Ada, E017, "langkit_support__boxes_E");
   E040 : Short_Integer; pragma Import (Ada, E040, "langkit_support__hashes_E");
   E042 : Short_Integer; pragma Import (Ada, E042, "langkit_support__images_E");
   E051 : Short_Integer; pragma Import (Ada, E051, "langkit_support__iterators_E");
   E060 : Short_Integer; pragma Import (Ada, E060, "langkit_support__packrat_E");
   E062 : Short_Integer; pragma Import (Ada, E062, "langkit_support__relative_get_E");
   E070 : Short_Integer; pragma Import (Ada, E070, "langkit_support__text_E");
   E058 : Short_Integer; pragma Import (Ada, E058, "langkit_support__names_E");
   E056 : Short_Integer; pragma Import (Ada, E056, "langkit_support__names__maps_E");
   E064 : Short_Integer; pragma Import (Ada, E064, "langkit_support__slocs_E");
   E027 : Short_Integer; pragma Import (Ada, E027, "langkit_support__diagnostics_E");
   E025 : Short_Integer; pragma Import (Ada, E025, "langkit_support__diagnostics__output_E");
   E030 : Short_Integer; pragma Import (Ada, E030, "langkit_support__file_readers_E");
   E077 : Short_Integer; pragma Import (Ada, E077, "langkit_support__vectors_E");
   E010 : Short_Integer; pragma Import (Ada, E010, "langkit_support__adalog__solver_E");
   E004 : Short_Integer; pragma Import (Ada, E004, "langkit_support__adalog__generic_main_support_E");
   E008 : Short_Integer; pragma Import (Ada, E008, "langkit_support__adalog__main_support_E");
   E023 : Short_Integer; pragma Import (Ada, E023, "langkit_support__cheap_sets_E");
   E038 : Short_Integer; pragma Import (Ada, E038, "langkit_support__generic_bump_ptr_E");
   E019 : Short_Integer; pragma Import (Ada, E019, "langkit_support__bump_ptr_E");
   E021 : Short_Integer; pragma Import (Ada, E021, "langkit_support__bump_ptr_vectors_E");
   E052 : Short_Integer; pragma Import (Ada, E052, "langkit_support__lexical_envs_E");
   E068 : Short_Integer; pragma Import (Ada, E068, "langkit_support__symbols_E");
   E054 : Short_Integer; pragma Import (Ada, E054, "langkit_support__lexical_envs_impl_E");
   E066 : Short_Integer; pragma Import (Ada, E066, "langkit_support__symbols__precomputed_E");
   E072 : Short_Integer; pragma Import (Ada, E072, "langkit_support__token_data_handlers_E");
   E036 : Short_Integer; pragma Import (Ada, E036, "langkit_support__generic_api_E");
   E044 : Short_Integer; pragma Import (Ada, E044, "langkit_support__internal__analysis_E");
   E032 : Short_Integer; pragma Import (Ada, E032, "langkit_support__generic_api__analysis_E");
   E034 : Short_Integer; pragma Import (Ada, E034, "langkit_support__generic_api__introspection_E");
   E048 : Short_Integer; pragma Import (Ada, E048, "langkit_support__internal__introspection_E");
   E074 : Short_Integer; pragma Import (Ada, E074, "langkit_support__tree_traversal_iterator_E");

   Sec_Default_Sized_Stacks : array (1 .. 1) of aliased System.Secondary_Stack.SS_Stack (System.Parameters.Runtime_Default_Sec_Stack_Size);

   Local_Priority_Specific_Dispatching : constant String := "";
   Local_Interrupt_States : constant String := "";

   Is_Elaborated : Boolean := False;

   procedure finalize_library is
   begin
      E048 := E048 - 1;
      E034 := E034 - 1;
      E032 := E032 - 1;
      declare
         procedure F1;
         pragma Import (Ada, F1, "langkit_support__internal__introspection__finalize_spec");
      begin
         if E048 = 0 then
            F1;
         end if;
      end;
      declare
         procedure F2;
         pragma Import (Ada, F2, "langkit_support__generic_api__introspection__finalize_spec");
      begin
         if E034 = 0 then
            F2;
         end if;
      end;
      declare
         procedure F3;
         pragma Import (Ada, F3, "langkit_support__generic_api__analysis__finalize_spec");
      begin
         if E032 = 0 then
            F3;
         end if;
      end;
      E072 := E072 - 1;
      declare
         procedure F4;
         pragma Import (Ada, F4, "langkit_support__token_data_handlers__finalize_spec");
      begin
         if E072 = 0 then
            F4;
         end if;
      end;
      E068 := E068 - 1;
      declare
         procedure F5;
         pragma Import (Ada, F5, "langkit_support__symbols__finalize_spec");
      begin
         if E068 = 0 then
            F5;
         end if;
      end;
      declare
         procedure F6;
         pragma Import (Ada, F6, "langkit_support__lexical_envs__finalize_spec");
      begin
         E052 := E052 - 1;
         if E052 = 0 then
            F6;
         end if;
      end;
      E030 := E030 - 1;
      declare
         procedure F7;
         pragma Import (Ada, F7, "langkit_support__file_readers__finalize_spec");
      begin
         if E030 = 0 then
            F7;
         end if;
      end;
      E027 := E027 - 1;
      declare
         procedure F8;
         pragma Import (Ada, F8, "langkit_support__diagnostics__finalize_spec");
      begin
         if E027 = 0 then
            F8;
         end if;
      end;
      declare
         procedure F9;
         pragma Import (Ada, F9, "gnatcoll__traces__finalize_body");
      begin
         E302 := E302 - 1;
         if E302 = 0 then
            F9;
         end if;
      end;
      declare
         procedure F10;
         pragma Import (Ada, F10, "gnatcoll__traces__finalize_spec");
      begin
         if E302 = 0 then
            F10;
         end if;
      end;
      E362 := E362 - 1;
      declare
         procedure F11;
         pragma Import (Ada, F11, "gnatcoll__vfs__finalize_spec");
      begin
         if E362 = 0 then
            F11;
         end if;
      end;
      E373 := E373 - 1;
      declare
         procedure F12;
         pragma Import (Ada, F12, "gnatcoll__io__remote__finalize_spec");
      begin
         if E373 = 0 then
            F12;
         end if;
      end;
      declare
         procedure F13;
         pragma Import (Ada, F13, "gnatcoll__remote__finalize_spec");
      begin
         E391 := E391 - 1;
         if E391 = 0 then
            F13;
         end if;
      end;
      E377 := E377 - 1;
      declare
         procedure F14;
         pragma Import (Ada, F14, "gnatcoll__io__native__finalize_spec");
      begin
         if E377 = 0 then
            F14;
         end if;
      end;
      E370 := E370 - 1;
      declare
         procedure F15;
         pragma Import (Ada, F15, "gnatcoll__io__finalize_spec");
      begin
         if E370 = 0 then
            F15;
         end if;
      end;
      E348 := E348 - 1;
      declare
         procedure F16;
         pragma Import (Ada, F16, "gnatcoll__terminal__finalize_spec");
      begin
         if E348 = 0 then
            F16;
         end if;
      end;
      E270 := E270 - 1;
      declare
         procedure F17;
         pragma Import (Ada, F17, "gnatcoll__refcount__finalize_spec");
      begin
         if E270 = 0 then
            F17;
         end if;
      end;
      declare
         procedure F18;
         pragma Import (Ada, F18, "gnatcoll__memory__finalize_body");
      begin
         E326 := E326 - 1;
         if E326 = 0 then
            F18;
         end if;
      end;
      E245 := E245 - 1;
      declare
         procedure F19;
         pragma Import (Ada, F19, "adasat__builders__finalize_spec");
      begin
         if E245 = 0 then
            F19;
         end if;
      end;
      declare
         procedure F20;
         pragma Import (Ada, F20, "adasat__internals__finalize_spec");
      begin
         E252 := E252 - 1;
         if E252 = 0 then
            F20;
         end if;
      end;
      E249 := E249 - 1;
      declare
         procedure F21;
         pragma Import (Ada, F21, "adasat__formulas__finalize_spec");
      begin
         if E249 = 0 then
            F21;
         end if;
      end;
      E415 := E415 - 1;
      declare
         procedure F22;
         pragma Import (Ada, F22, "gnatcoll__gmp__integers__finalize_spec");
      begin
         if E415 = 0 then
            F22;
         end if;
      end;
      declare
         procedure F23;
         pragma Import (Ada, F23, "gnat__debug_pools__finalize_body");
      begin
         E328 := E328 - 1;
         if E328 = 0 then
            F23;
         end if;
      end;
      declare
         procedure F24;
         pragma Import (Ada, F24, "gnat__debug_pools__finalize_spec");
      begin
         if E328 = 0 then
            F24;
         end if;
      end;
      declare
         procedure F25;
         pragma Import (Ada, F25, "ada__directories__finalize_body");
      begin
         E379 := E379 - 1;
         if E379 = 0 then
            F25;
         end if;
      end;
      declare
         procedure F26;
         pragma Import (Ada, F26, "ada__directories__finalize_spec");
      begin
         if E379 = 0 then
            F26;
         end if;
      end;
      E386 := E386 - 1;
      declare
         procedure F27;
         pragma Import (Ada, F27, "system__regexp__finalize_spec");
      begin
         if E386 = 0 then
            F27;
         end if;
      end;
      E357 := E357 - 1;
      declare
         procedure F28;
         pragma Import (Ada, F28, "gnat__expect__finalize_spec");
      begin
         if E357 = 0 then
            F28;
         end if;
      end;
      E279 := E279 - 1;
      declare
         procedure F29;
         pragma Import (Ada, F29, "system__pool_global__finalize_spec");
      begin
         if E279 = 0 then
            F29;
         end if;
      end;
      E193 := E193 - 1;
      declare
         procedure F30;
         pragma Import (Ada, F30, "ada__text_io__finalize_spec");
      begin
         if E193 = 0 then
            F30;
         end if;
      end;
      E418 := E418 - 1;
      declare
         procedure F31;
         pragma Import (Ada, F31, "ada__strings__wide_wide_unbounded__finalize_spec");
      begin
         if E418 = 0 then
            F31;
         end if;
      end;
      E422 := E422 - 1;
      declare
         procedure F32;
         pragma Import (Ada, F32, "ada__strings__wide_wide_maps__finalize_spec");
      begin
         if E422 = 0 then
            F32;
         end if;
      end;
      E227 := E227 - 1;
      declare
         procedure F33;
         pragma Import (Ada, F33, "ada__strings__unbounded__finalize_spec");
      begin
         if E227 = 0 then
            F33;
         end if;
      end;
      E298 := E298 - 1;
      declare
         procedure F34;
         pragma Import (Ada, F34, "system__storage_pools__subpools__finalize_spec");
      begin
         if E298 = 0 then
            F34;
         end if;
      end;
      E277 := E277 - 1;
      declare
         procedure F35;
         pragma Import (Ada, F35, "system__finalization_masters__finalize_spec");
      begin
         if E277 = 0 then
            F35;
         end if;
      end;
      declare
         procedure F36;
         pragma Import (Ada, F36, "system__file_io__finalize_body");
      begin
         E203 := E203 - 1;
         if E203 = 0 then
            F36;
         end if;
      end;
      declare
         procedure Reraise_Library_Exception_If_Any;
            pragma Import (Ada, Reraise_Library_Exception_If_Any, "__gnat_reraise_library_exception_if_any");
      begin
         Reraise_Library_Exception_If_Any;
      end;
   end finalize_library;

   procedure langkit_supportfinal is

      procedure Runtime_Finalize;
      pragma Import (C, Runtime_Finalize, "__gnat_runtime_finalize");

   begin
      if not Is_Elaborated then
         return;
      end if;
      Is_Elaborated := False;
      Runtime_Finalize;
      finalize_library;
   end langkit_supportfinal;

   type No_Param_Proc is access procedure;
   pragma Favor_Top_Level (No_Param_Proc);

   procedure langkit_supportinit is
      Main_Priority : Integer;
      pragma Import (C, Main_Priority, "__gl_main_priority");
      Time_Slice_Value : Integer;
      pragma Import (C, Time_Slice_Value, "__gl_time_slice_val");
      WC_Encoding : Character;
      pragma Import (C, WC_Encoding, "__gl_wc_encoding");
      Locking_Policy : Character;
      pragma Import (C, Locking_Policy, "__gl_locking_policy");
      Queuing_Policy : Character;
      pragma Import (C, Queuing_Policy, "__gl_queuing_policy");
      Task_Dispatching_Policy : Character;
      pragma Import (C, Task_Dispatching_Policy, "__gl_task_dispatching_policy");
      Priority_Specific_Dispatching : System.Address;
      pragma Import (C, Priority_Specific_Dispatching, "__gl_priority_specific_dispatching");
      Num_Specific_Dispatching : Integer;
      pragma Import (C, Num_Specific_Dispatching, "__gl_num_specific_dispatching");
      Main_CPU : Integer;
      pragma Import (C, Main_CPU, "__gl_main_cpu");
      Interrupt_States : System.Address;
      pragma Import (C, Interrupt_States, "__gl_interrupt_states");
      Num_Interrupt_States : Integer;
      pragma Import (C, Num_Interrupt_States, "__gl_num_interrupt_states");
      Unreserve_All_Interrupts : Integer;
      pragma Import (C, Unreserve_All_Interrupts, "__gl_unreserve_all_interrupts");
      Detect_Blocking : Integer;
      pragma Import (C, Detect_Blocking, "__gl_detect_blocking");
      Default_Stack_Size : Integer;
      pragma Import (C, Default_Stack_Size, "__gl_default_stack_size");
      Default_Secondary_Stack_Size : System.Parameters.Size_Type;
      pragma Import (C, Default_Secondary_Stack_Size, "__gnat_default_ss_size");
      Bind_Env_Addr : System.Address;
      pragma Import (C, Bind_Env_Addr, "__gl_bind_env_addr");

      procedure Runtime_Initialize (Install_Handler : Integer);
      pragma Import (C, Runtime_Initialize, "__gnat_runtime_initialize");

      Finalize_Library_Objects : No_Param_Proc;
      pragma Import (C, Finalize_Library_Objects, "__gnat_finalize_library_objects");
      Binder_Sec_Stacks_Count : Natural;
      pragma Import (Ada, Binder_Sec_Stacks_Count, "__gnat_binder_ss_count");
      Default_Sized_SS_Pool : System.Address;
      pragma Import (Ada, Default_Sized_SS_Pool, "__gnat_default_ss_pool");

   begin
      if Is_Elaborated then
         return;
      end if;
      Is_Elaborated := True;
      Main_Priority := -1;
      Time_Slice_Value := -1;
      WC_Encoding := 'b';
      Locking_Policy := ' ';
      Queuing_Policy := ' ';
      Task_Dispatching_Policy := ' ';
      Priority_Specific_Dispatching :=
        Local_Priority_Specific_Dispatching'Address;
      Num_Specific_Dispatching := 0;
      Main_CPU := -1;
      Interrupt_States := Local_Interrupt_States'Address;
      Num_Interrupt_States := 0;
      Unreserve_All_Interrupts := 0;
      Detect_Blocking := 0;
      Default_Stack_Size := -1;

      langkit_supportmain'Elab_Body;
      Default_Secondary_Stack_Size := System.Parameters.Runtime_Default_Sec_Stack_Size;
      Binder_Sec_Stacks_Count := 1;
      Default_Sized_SS_Pool := Sec_Default_Sized_Stacks'Address;

      Runtime_Initialize (1);

      if E093 = 0 then
         Ada.Exceptions'Elab_Spec;
      end if;
      if E089 = 0 then
         System.Soft_Links'Elab_Spec;
      end if;
      if E087 = 0 then
         System.Exception_Table'Elab_Body;
      end if;
      E087 := E087 + 1;
      if E120 = 0 then
         Ada.Containers'Elab_Spec;
      end if;
      E120 := E120 + 1;
      if E149 = 0 then
         Ada.Io_Exceptions'Elab_Spec;
      end if;
      E149 := E149 + 1;
      if E102 = 0 then
         Ada.Numerics'Elab_Spec;
      end if;
      E102 := E102 + 1;
      if E084 = 0 then
         Ada.Strings'Elab_Spec;
      end if;
      E084 := E084 + 1;
      if E138 = 0 then
         Ada.Strings.Maps'Elab_Spec;
      end if;
      E138 := E138 + 1;
      if E141 = 0 then
         Ada.Strings.Maps.Constants'Elab_Spec;
      end if;
      E141 := E141 + 1;
      if E125 = 0 then
         Interfaces.C'Elab_Spec;
      end if;
      E125 := E125 + 1;
      if E096 = 0 then
         System.Exceptions'Elab_Spec;
      end if;
      E096 := E096 + 1;
      if E163 = 0 then
         System.Object_Reader'Elab_Spec;
      end if;
      E163 := E163 + 1;
      if E132 = 0 then
         System.Dwarf_Lines'Elab_Spec;
      end if;
      if E154 = 0 then
         System.Os_Lib'Elab_Body;
      end if;
      E154 := E154 + 1;
      if E177 = 0 then
         System.Soft_Links.Initialize'Elab_Body;
      end if;
      E177 := E177 + 1;
      E089 := E089 + 1;
      if E119 = 0 then
         System.Traceback.Symbolic'Elab_Body;
      end if;
      E119 := E119 + 1;
      if E101 = 0 then
         System.Img_Int'Elab_Spec;
      end if;
      E101 := E101 + 1;
      E093 := E093 + 1;
      if E144 = 0 then
         System.Img_Uns'Elab_Spec;
      end if;
      E144 := E144 + 1;
      E132 := E132 + 1;
      if E217 = 0 then
         Ada.Assertions'Elab_Spec;
      end if;
      E217 := E217 + 1;
      if E181 = 0 then
         Ada.Strings.Utf_Encoding'Elab_Spec;
      end if;
      E181 := E181 + 1;
      if E187 = 0 then
         Ada.Tags'Elab_Spec;
      end if;
      if E187 = 0 then
         Ada.Tags'Elab_Body;
      end if;
      E187 := E187 + 1;
      if E083 = 0 then
         Ada.Strings.Text_Buffers'Elab_Spec;
      end if;
      E083 := E083 + 1;
      if E258 = 0 then
         Gnat'Elab_Spec;
      end if;
      E258 := E258 + 1;
      if E213 = 0 then
         Interfaces.C.Strings'Elab_Spec;
      end if;
      E213 := E213 + 1;
      if E195 = 0 then
         Ada.Streams'Elab_Spec;
      end if;
      E195 := E195 + 1;
      if E207 = 0 then
         System.File_Control_Block'Elab_Spec;
      end if;
      E207 := E207 + 1;
      if E206 = 0 then
         System.Finalization_Root'Elab_Spec;
      end if;
      E206 := E206 + 1;
      if E204 = 0 then
         Ada.Finalization'Elab_Spec;
      end if;
      E204 := E204 + 1;
      if E203 = 0 then
         System.File_Io'Elab_Body;
      end if;
      E203 := E203 + 1;
      if E322 = 0 then
         System.Regpat'Elab_Spec;
      end if;
      E322 := E322 + 1;
      if E275 = 0 then
         System.Storage_Pools'Elab_Spec;
      end if;
      E275 := E275 + 1;
      if E277 = 0 then
         System.Finalization_Masters'Elab_Spec;
      end if;
      if E277 = 0 then
         System.Finalization_Masters'Elab_Body;
      end if;
      E277 := E277 + 1;
      if E298 = 0 then
         System.Storage_Pools.Subpools'Elab_Spec;
      end if;
      E298 := E298 + 1;
      if E227 = 0 then
         Ada.Strings.Unbounded'Elab_Spec;
      end if;
      E227 := E227 + 1;
      if E422 = 0 then
         Ada.Strings.Wide_Wide_Maps'Elab_Spec;
      end if;
      E422 := E422 + 1;
      if E418 = 0 then
         Ada.Strings.Wide_Wide_Unbounded'Elab_Spec;
      end if;
      E418 := E418 + 1;
      if E219 = 0 then
         Ada.Calendar'Elab_Spec;
      end if;
      if E219 = 0 then
         Ada.Calendar'Elab_Body;
      end if;
      E219 := E219 + 1;
      if E407 = 0 then
         Ada.Calendar.Delays'Elab_Body;
      end if;
      E407 := E407 + 1;
      if E306 = 0 then
         Ada.Calendar.Time_Zones'Elab_Spec;
      end if;
      E306 := E306 + 1;
      if E193 = 0 then
         Ada.Text_Io'Elab_Spec;
      end if;
      if E193 = 0 then
         Ada.Text_Io'Elab_Body;
      end if;
      E193 := E193 + 1;
      E403 := E403 + 1;
      if E311 = 0 then
         Gnat.Calendar'Elab_Spec;
      end if;
      E311 := E311 + 1;
      if E375 = 0 then
         Gnat.Directory_Operations'Elab_Spec;
      end if;
      if E375 = 0 then
         Gnat.Directory_Operations'Elab_Body;
      end if;
      E375 := E375 + 1;
      if E339 = 0 then
         System.Checked_Pools'Elab_Spec;
      end if;
      E339 := E339 + 1;
      if E279 = 0 then
         System.Pool_Global'Elab_Spec;
      end if;
      if E279 = 0 then
         System.Pool_Global'Elab_Body;
      end if;
      E279 := E279 + 1;
      if E357 = 0 then
         Gnat.Expect'Elab_Spec;
      end if;
      if E357 = 0 then
         Gnat.Expect'Elab_Body;
      end if;
      E357 := E357 + 1;
      if E399 = 0 then
         System.Random_Seed'Elab_Body;
      end if;
      E399 := E399 + 1;
      if E386 = 0 then
         System.Regexp'Elab_Spec;
      end if;
      if E386 = 0 then
         System.Regexp'Elab_Body;
      end if;
      E386 := E386 + 1;
      if E379 = 0 then
         Ada.Directories'Elab_Spec;
      end if;
      if E379 = 0 then
         Ada.Directories'Elab_Body;
      end if;
      E379 := E379 + 1;
      if E316 = 0 then
         System.Img_Lli'Elab_Spec;
      end if;
      E316 := E316 + 1;
      if E318 = 0 then
         System.Img_Llu'Elab_Spec;
      end if;
      E318 := E318 + 1;
      if E314 = 0 then
         Gnat.Calendar.Time_Io'Elab_Spec;
      end if;
      E314 := E314 + 1;
      if E328 = 0 then
         Gnat.Debug_Pools'Elab_Spec;
      end if;
      if E328 = 0 then
         Gnat.Debug_Pools'Elab_Body;
      end if;
      E328 := E328 + 1;
      if E415 = 0 then
         GNATCOLL.GMP.INTEGERS'ELAB_SPEC;
      end if;
      E415 := E415 + 1;
      if E028 = 0 then
         Langkit_Support.Errors'Elab_Spec;
      end if;
      E028 := E028 + 1;
      E243 := E243 + 1;
      E254 := E254 + 1;
      E251 := E251 + 1;
      if E249 = 0 then
         Adasat.Formulas'Elab_Spec;
      end if;
      E249 := E249 + 1;
      if E252 = 0 then
         Adasat.Internals'Elab_Spec;
      end if;
      E252 := E252 + 1;
      if E245 = 0 then
         Adasat.Builders'Elab_Spec;
      end if;
      if E245 = 0 then
         Adasat.Builders'Elab_Body;
      end if;
      E245 := E245 + 1;
      E256 := E256 + 1;
      E266 := E266 + 1;
      if E326 = 0 then
         GNATCOLL.MEMORY'ELAB_BODY;
      end if;
      E326 := E326 + 1;
      if E353 = 0 then
         GNATCOLL.OS'ELAB_SPEC;
      end if;
      E353 := E353 + 1;
      E272 := E272 + 1;
      if E270 = 0 then
         GNATCOLL.REFCOUNT'ELAB_SPEC;
      end if;
      E270 := E270 + 1;
      E352 := E352 + 1;
      E268 := E268 + 1;
      if E264 = 0 then
         GNATCOLL.STRINGS'ELAB_SPEC;
      end if;
      if E264 = 0 then
         GNATCOLL.STRINGS'ELAB_BODY;
      end if;
      E264 := E264 + 1;
      if E341 = 0 then
         GNATCOLL.MMAP'ELAB_SPEC;
      end if;
      E343 := E343 + 1;
      E341 := E341 + 1;
      if E346 = 0 then
         GNATCOLL.TEMPLATES'ELAB_SPEC;
      end if;
      E346 := E346 + 1;
      if E348 = 0 then
         GNATCOLL.TERMINAL'ELAB_SPEC;
      end if;
      if E348 = 0 then
         GNATCOLL.TERMINAL'ELAB_BODY;
      end if;
      E348 := E348 + 1;
      E350 := E350 + 1;
      if E370 = 0 then
         GNATCOLL.IO'ELAB_SPEC;
      end if;
      if E370 = 0 then
         GNATCOLL.IO'ELAB_BODY;
      end if;
      E370 := E370 + 1;
      if E388 = 0 then
         GNATCOLL.PATH'ELAB_SPEC;
      end if;
      if E388 = 0 then
         GNATCOLL.PATH'ELAB_BODY;
      end if;
      E388 := E388 + 1;
      if E377 = 0 then
         GNATCOLL.IO.NATIVE'ELAB_SPEC;
      end if;
      if E377 = 0 then
         GNATCOLL.IO.NATIVE'ELAB_BODY;
      end if;
      E377 := E377 + 1;
      if E391 = 0 then
         GNATCOLL.REMOTE'ELAB_SPEC;
      end if;
      E391 := E391 + 1;
      if E395 = 0 then
         GNATCOLL.REMOTE.DB'ELAB_SPEC;
      end if;
      E395 := E395 + 1;
      if E373 = 0 then
         GNATCOLL.IO.REMOTE'ELAB_SPEC;
      end if;
      E390 := E390 + 1;
      E393 := E393 + 1;
      if E373 = 0 then
         GNATCOLL.IO.REMOTE'ELAB_BODY;
      end if;
      E373 := E373 + 1;
      if E362 = 0 then
         GNATCOLL.VFS'ELAB_SPEC;
      end if;
      if E362 = 0 then
         GNATCOLL.VFS'ELAB_BODY;
      end if;
      E362 := E362 + 1;
      if E302 = 0 then
         GNATCOLL.TRACES'ELAB_SPEC;
      end if;
      if E302 = 0 then
         GNATCOLL.TRACES'ELAB_BODY;
      end if;
      E302 := E302 + 1;
      if E405 = 0 then
         GNATCOLL.ICONV'ELAB_SPEC;
      end if;
      if E405 = 0 then
         GNATCOLL.ICONV'ELAB_BODY;
      end if;
      E405 := E405 + 1;
      if E013 = 0 then
         Langkit_Support.Adalog'Elab_Spec;
      end if;
      E013 := E013 + 1;
      E002 := E002 + 1;
      E006 := E006 + 1;
      E012 := E012 + 1;
      E015 := E015 + 1;
      E017 := E017 + 1;
      E040 := E040 + 1;
      E042 := E042 + 1;
      E051 := E051 + 1;
      E060 := E060 + 1;
      E062 := E062 + 1;
      if E070 = 0 then
         Langkit_Support.Text'Elab_Spec;
      end if;
      E070 := E070 + 1;
      if E058 = 0 then
         Langkit_Support.Names'Elab_Spec;
      end if;
      E058 := E058 + 1;
      E056 := E056 + 1;
      E064 := E064 + 1;
      if E027 = 0 then
         Langkit_Support.Diagnostics'Elab_Spec;
      end if;
      E027 := E027 + 1;
      if E025 = 0 then
         Langkit_Support.Diagnostics.Output'Elab_Spec;
      end if;
      if E025 = 0 then
         Langkit_Support.Diagnostics.Output'Elab_Body;
      end if;
      E025 := E025 + 1;
      if E030 = 0 then
         Langkit_Support.File_Readers'Elab_Spec;
      end if;
      E030 := E030 + 1;
      E077 := E077 + 1;
      E010 := E010 + 1;
      E004 := E004 + 1;
      if E008 = 0 then
         Langkit_Support.Adalog.Main_Support'Elab_Spec;
      end if;
      E008 := E008 + 1;
      E023 := E023 + 1;
      E038 := E038 + 1;
      if E019 = 0 then
         Langkit_Support.Bump_Ptr'Elab_Spec;
      end if;
      E019 := E019 + 1;
      E021 := E021 + 1;
      if E052 = 0 then
         Langkit_Support.Lexical_Envs'Elab_Spec;
      end if;
      E052 := E052 + 1;
      if E068 = 0 then
         Langkit_Support.Symbols'Elab_Spec;
      end if;
      E068 := E068 + 1;
      E054 := E054 + 1;
      E066 := E066 + 1;
      if E072 = 0 then
         Langkit_Support.Token_Data_Handlers'Elab_Spec;
      end if;
      E072 := E072 + 1;
      if E036 = 0 then
         Langkit_Support.Generic_Api'Elab_Spec;
      end if;
      if E032 = 0 then
         Langkit_Support.Generic_Api.Analysis'Elab_Spec;
      end if;
      if E034 = 0 then
         Langkit_Support.Generic_Api.Introspection'Elab_Spec;
      end if;
      if E048 = 0 then
         Langkit_Support.Internal.Introspection'Elab_Spec;
      end if;
      E036 := E036 + 1;
      if E032 = 0 then
         Langkit_Support.Generic_Api.Analysis'Elab_Body;
      end if;
      E032 := E032 + 1;
      if E034 = 0 then
         Langkit_Support.Generic_Api.Introspection'Elab_Body;
      end if;
      E034 := E034 + 1;
      E044 := E044 + 1;
      if E048 = 0 then
         Langkit_Support.Internal.Introspection'Elab_Body;
      end if;
      E048 := E048 + 1;
      E074 := E074 + 1;
   end langkit_supportinit;

--  BEGIN Object file/option list
   --   /data/devel/eng/recordflux/RecordFlux/src/langkit/langkit/support/obj/dev/langkit_support.o
   --   /data/devel/eng/recordflux/RecordFlux/src/langkit/langkit/support/obj/dev/langkit_support-errors.o
   --   /data/devel/eng/recordflux/RecordFlux/src/langkit/langkit/support/obj/dev/langkit_support-adalog.o
   --   /data/devel/eng/recordflux/RecordFlux/src/langkit/langkit/support/obj/dev/langkit_support-adalog-debug.o
   --   /data/devel/eng/recordflux/RecordFlux/src/langkit/langkit/support/obj/dev/langkit_support-adalog-logic_var.o
   --   /data/devel/eng/recordflux/RecordFlux/src/langkit/langkit/support/obj/dev/langkit_support-adalog-solver_interface.o
   --   /data/devel/eng/recordflux/RecordFlux/src/langkit/langkit/support/obj/dev/langkit_support-array_utils.o
   --   /data/devel/eng/recordflux/RecordFlux/src/langkit/langkit/support/obj/dev/langkit_support-boxes.o
   --   /data/devel/eng/recordflux/RecordFlux/src/langkit/langkit/support/obj/dev/langkit_support-hashes.o
   --   /data/devel/eng/recordflux/RecordFlux/src/langkit/langkit/support/obj/dev/langkit_support-images.o
   --   /data/devel/eng/recordflux/RecordFlux/src/langkit/langkit/support/obj/dev/langkit_support-iterators.o
   --   /data/devel/eng/recordflux/RecordFlux/src/langkit/langkit/support/obj/dev/langkit_support-packrat.o
   --   /data/devel/eng/recordflux/RecordFlux/src/langkit/langkit/support/obj/dev/langkit_support-relative_get.o
   --   /data/devel/eng/recordflux/RecordFlux/src/langkit/langkit/support/obj/dev/langkit_support-text.o
   --   /data/devel/eng/recordflux/RecordFlux/src/langkit/langkit/support/obj/dev/langkit_support-names.o
   --   /data/devel/eng/recordflux/RecordFlux/src/langkit/langkit/support/obj/dev/langkit_support-names-maps.o
   --   /data/devel/eng/recordflux/RecordFlux/src/langkit/langkit/support/obj/dev/langkit_support-slocs.o
   --   /data/devel/eng/recordflux/RecordFlux/src/langkit/langkit/support/obj/dev/langkit_support-diagnostics.o
   --   /data/devel/eng/recordflux/RecordFlux/src/langkit/langkit/support/obj/dev/langkit_support-diagnostics-output.o
   --   /data/devel/eng/recordflux/RecordFlux/src/langkit/langkit/support/obj/dev/langkit_support-file_readers.o
   --   /data/devel/eng/recordflux/RecordFlux/src/langkit/langkit/support/obj/dev/langkit_support-types.o
   --   /data/devel/eng/recordflux/RecordFlux/src/langkit/langkit/support/obj/dev/langkit_support-vectors.o
   --   /data/devel/eng/recordflux/RecordFlux/src/langkit/langkit/support/obj/dev/langkit_support-adalog-solver.o
   --   /data/devel/eng/recordflux/RecordFlux/src/langkit/langkit/support/obj/dev/langkit_support-adalog-generic_main_support.o
   --   /data/devel/eng/recordflux/RecordFlux/src/langkit/langkit/support/obj/dev/langkit_support-adalog-main_support.o
   --   /data/devel/eng/recordflux/RecordFlux/src/langkit/langkit/support/obj/dev/langkit_support-cheap_sets.o
   --   /data/devel/eng/recordflux/RecordFlux/src/langkit/langkit/support/obj/dev/langkit_support-generic_bump_ptr.o
   --   /data/devel/eng/recordflux/RecordFlux/src/langkit/langkit/support/obj/dev/langkit_support-bump_ptr.o
   --   /data/devel/eng/recordflux/RecordFlux/src/langkit/langkit/support/obj/dev/langkit_support-bump_ptr_vectors.o
   --   /data/devel/eng/recordflux/RecordFlux/src/langkit/langkit/support/obj/dev/langkit_support-lexical_envs.o
   --   /data/devel/eng/recordflux/RecordFlux/src/langkit/langkit/support/obj/dev/langkit_support-symbols.o
   --   /data/devel/eng/recordflux/RecordFlux/src/langkit/langkit/support/obj/dev/langkit_support-lexical_envs_impl.o
   --   /data/devel/eng/recordflux/RecordFlux/src/langkit/langkit/support/obj/dev/langkit_support-symbols-precomputed.o
   --   /data/devel/eng/recordflux/RecordFlux/src/langkit/langkit/support/obj/dev/langkit_support-token_data_handlers.o
   --   /data/devel/eng/recordflux/RecordFlux/src/langkit/langkit/support/obj/dev/langkit_support-internal.o
   --   /data/devel/eng/recordflux/RecordFlux/src/langkit/langkit/support/obj/dev/langkit_support-internal-conversions.o
   --   /data/devel/eng/recordflux/RecordFlux/src/langkit/langkit/support/obj/dev/langkit_support-internal-descriptor.o
   --   /data/devel/eng/recordflux/RecordFlux/src/langkit/langkit/support/obj/dev/langkit_support-generic_api.o
   --   /data/devel/eng/recordflux/RecordFlux/src/langkit/langkit/support/obj/dev/langkit_support-generic_api-analysis.o
   --   /data/devel/eng/recordflux/RecordFlux/src/langkit/langkit/support/obj/dev/langkit_support-generic_api-introspection.o
   --   /data/devel/eng/recordflux/RecordFlux/src/langkit/langkit/support/obj/dev/langkit_support-internal-analysis.o
   --   /data/devel/eng/recordflux/RecordFlux/src/langkit/langkit/support/obj/dev/langkit_support-internal-introspection.o
   --   /data/devel/eng/recordflux/RecordFlux/src/langkit/langkit/support/obj/dev/langkit_support-tree_traversal_iterator.o
   --   -L/data/devel/eng/recordflux/RecordFlux/src/langkit/langkit/support/obj/dev/
   --   -L/data/devel/eng/recordflux/RecordFlux/src/adasat/lib/static-pic/dev/
   --   -L/data/devel/eng/recordflux/RecordFlux/src/gnatcoll-bindings/iconv/lib/static-pic/
   --   -L/data/devel/eng/recordflux/RecordFlux/src/gnatcoll-bindings/gmp/lib/static-pic/
   --   -L/opt/gnatpro/23.0w-20220718/lib/xmlada/xmlada_dom.static-pic/
   --   -L/opt/gnatpro/23.0w-20220718/lib/xmlada/xmlada_schema.static-pic/
   --   -L/opt/gnatpro/23.0w-20220718/lib/xmlada/xmlada_unicode.static-pic/
   --   -L/opt/gnatpro/23.0w-20220718/lib/xmlada/xmlada_input.static-pic/
   --   -L/opt/gnatpro/23.0w-20220718/lib/xmlada/xmlada_sax.static-pic/
   --   -L/opt/gnatpro/23.0w-20220718/lib/gpr/static-pic/gpr/
   --   -L/opt/gnatpro/23.0w-20220718/lib/gnatcoll.static-pic/
   --   -L/opt/gnatpro/23.0w-20220718/lib/gcc/x86_64-pc-linux-gnu/11.3.1/adalib/
   --   -static
   --   -lgnat
   --   -ldl
--  END Object file/option list   

end langkit_supportmain;
